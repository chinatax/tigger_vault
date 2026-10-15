#!/usr/bin/env python3
# coding=utf-8
"""把 tax-policy-crawler 抓下的「国家税务总局政策法规库」条目，落成 raw/ 素材。

输入：/home/tigger/codes/tax-policy-crawler/tax_policy.jsonl（一行一条 JSON）
输出：raw/制度/国家税收政策法规/<标题>（<文号>）.txt

格式照 raw/制度/安徽地方税收法规/ 的既有约定：纯 .txt + 【字段】文本头，
**不用 YAML frontmatter**（该目录 2026-09-29 新建的文件是真实约定）。

正文逐字节照录自 jsonl 的 content 字段，不做任何清洗/改写——raw/ 只增不改。

用法：
    python3 scripts/import-zcfgk-raw.py --dry-run --limit 30   # 只看会生成什么，不落盘
    python3 scripts/import-zcfgk-raw.py --limit 30             # 试点 30 条
    python3 scripts/import-zcfgk-raw.py                        # 全量（试点通过后再跑）

过滤：排除源站标注失效的，以及源站漏标的连带失效件。详见 DEAD_AGING / LINKED_DEAD_TITLES。
"""
import argparse
import hashlib
import json
import os
import re
import sys

DEFAULT_JSONL = '/home/tigger/codes/tax-policy-crawler/tax_policy.jsonl'
DEFAULT_OUTDIR = 'raw/制度/国家税收政策法规'
CRAWL_DATE = '2026-09-29'

# 源站明确标注失效的时效值
DEAD_AGING = ('全文废止', '全文失效')

# 源站标了"条例"那层、却没连带标注"实施细则/配套通知"那层——母条例已废止，这些实际也失效。
# 判断模式：母法已废止 → 其实施细则/配套通知必死。用户 2026-09-29 已逐条确认。
# 注意别把「土地增值税暂行条例实施细则」误加进来：它母条例是有效的。
LINKED_DEAD_TITLES = {
    '中华人民共和国集体企业所得税暂行条例施行细则',
    '中华人民共和国私营企业所得税暂行条例施行细则',
    '中华人民共和国印花税暂行条例施行细则',
    '中华人民共和国企业所得税暂行条例实施细则',
    '中华人民共和国车船税暂行条例实施细则',
    '中华人民共和国耕地占用税暂行条例实施细则',
    '中华人民共和国增值税暂行条例实施细则',
    '中华人民共和国契税暂行条例细则',
    '财政部 国家税务总局关于贯彻落实《中华人民共和国车船税暂行条例》及其实施细则有关问题的通知',
    '财政部 国家税务总局关于贯彻落实车船税暂行条例工作有关问题的通知',
    # 其母办法《增值税一般纳税人登记管理办法》已被废止（该办法本身已被 DEAD_AGING 剔除），
    # 这份解读解读的就是那个已废止的办法，内容失效。用户 2026-09-29 裁定剔除。
    # 注意别误伤「关于《国家税务总局关于废止〈增值税一般纳税人登记管理办法〉的决定》的解读」——
    # 那份解读的是废止决定本身，仍然有效，字面量也不同（《》 vs 〈〉）。
    '关于《增值税一般纳税人登记管理办法》的解读',
}

# 文件名里不能出现的字符 → 全角对应（ext4 允许中文，只是这几个 ASCII 字符有特殊含义）
ILLEGAL_CHARS = {'/': '／', '\\': '＼', ':': '：', '*': '＊', '?': '？',
                 '"': '＂', '<': '＜', '>': '＞', '|': '｜', '\x00': ''}
# 标题/文号里若混进换行会把【】头撑坏，先行压平
WHITESPACE_RE = re.compile(r'[\r\n\t]+')
NAME_MAX_BYTES = 250     # ext4 单个文件名上限 255 字节，留点余量给 ".txt" 和重名后缀


def load(jsonl_path):
    with open(jsonl_path, encoding='utf-8') as fp:
        for line in fp:
            line = line.strip()
            if line:
                yield json.loads(line)


def keep(doc):
    """是否保留该条。返回 (bool, 原因)。"""
    if (doc.get('aging') or '') in DEAD_AGING:
        return False, '源站标注失效：' + doc['aging']
    if (doc.get('title') or '').strip() in LINKED_DEAD_TITLES:
        return False, '连带失效：所依据的母法已废止'
    if not (doc.get('content') or '').strip():
        return False, '无正文'
    return True, ''


def flat(value):
    """字段值压平：去换行/制表，去掉接口里的 'null' 字面量。"""
    text = WHITESPACE_RE.sub(' ', str(value if value is not None else '')).strip()
    return '' if text == 'null' else text


def shorten(stem):
    """超长标题压到 NAME_MAX_BYTES 内：保留头 40% + 尾 60%，尾部才是文档名。

    ext4 单段 255 字节，中文一字 3 字节。这类长标题的结构基本是
    「<十几个部委>关于<某事>的通知」——有价值的是尾部，砍尾等于把文件名废掉。
    末尾挂标题 sha1 前 8 位，保证截断后仍可区分。
    """
    digest = hashlib.sha1(stem.encode('utf-8')).hexdigest()[:8]
    fixed = len(('.txt').encode('utf-8')) + len(('-{}'.format(digest)).encode('utf-8')) \
        + len('…'.encode('utf-8'))
    budget = NAME_MAX_BYTES - fixed
    head_len = max(24, budget * 2 // 5)
    tail_len = budget - head_len
    raw = stem.encode('utf-8')
    head = raw[:head_len].decode('utf-8', 'ignore').rstrip()
    tail = raw[-tail_len:].decode('utf-8', 'ignore') if tail_len > 0 else ''
    out = '{head}…{tail}-{digest}'.format(head=head, tail=tail, digest=digest)
    while len(out.encode('utf-8')) > NAME_MAX_BYTES:   # 多字节边界兜底
        head = head[:-1]
        out = '{head}…{tail}-{digest}'.format(head=head, tail=tail, digest=digest)
    return out


def filename_for(doc, taken):
    """按知识库既有约定造文件名：<标题>（<文号>）.txt；重名追加 -2 序号。"""
    title = flat(doc.get('title'))
    subtitle = flat(doc.get('subtitle'))
    stem = '{}（{}）'.format(title, subtitle) if subtitle else title
    for bad, good in ILLEGAL_CHARS.items():
        stem = stem.replace(bad, good)
    if len(('{}.txt'.format(stem)).encode('utf-8')) > NAME_MAX_BYTES:
        stem = shorten(stem)
    name = '{}.txt'.format(stem)
    if name in taken:                       # 「标题+文号」重名：追加序号
        n = 2
        while '{}-{}.txt'.format(stem, n) in taken:
            n += 1
        name = '{}-{}.txt'.format(stem, n)
    return name


def assign_names(docs):
    """给**全部**条目统一分配文件名，返回 {url: name}。

    必须一次算完，不能只算本次要输出的那些：否则试点（--limit 30）和全量
    对同一条重名文档可能分配不同的 -2 后缀，落盘后会残留两份重复文件。
    """
    names, taken = {}, set()
    for doc in docs:
        name = filename_for(doc, taken)
        taken.add(name)
        names[doc['url']] = name
    return names


def render(doc):
    """渲染成 raw 文件内容。正文原样照录，只在末尾补一个换行。"""
    title = flat(doc.get('title'))
    subtitle = flat(doc.get('subtitle'))
    date = flat(doc.get('date'))

    lines = ['【标题】' + title]
    if subtitle:
        lines.append('【文号】' + subtitle)
    lines.append('【来源】' + flat(doc.get('url')))
    lines.append('【抓取】{} 由 Claude Code 自国税总局政策法规库抓取，供检索使用；'
                 '正式引用请核对原文（见【来源】）'.format(CRAWL_DATE))

    # 时效始终写全。源站未标注的（占大多数）不替它写成"全文有效"——那等于伪造字段值；
    # 如实记「未标注」再标出我们的处理口径（用户裁定：未标注即现行有效），既保真又可审计。
    aging = flat(doc.get('aging'))
    notes = ['时效：' + (aging if aging else '未标注（按现行有效）')]
    # 成文日期（接口的 cwrq，站点搜索表单标签即「成文日期」，非发布日期/入库日期）。
    # 放进备注是为了区分同名多版本的解读：如某解读有 2014/2019/2025/2026 四版，
    # 文件名只差 -2/-3/-4，光看名字认不出哪版最新。
    if flat(doc.get('date')):
        notes.append('成文日期：' + flat(doc['date']))
    if doc.get('taxLevel'):
        # 字段名取自爬虫的 taxLevel，但站点对该字段的注释是「税费政策类型」，
        # 取值是 税收政策/非税收入政策/社会保险费政策/税费征管/其他——不是税种，别照着字段名写。
        notes.append('税费政策类型：' + flat(doc['taxLevel']))
    if doc.get('publisher'):
        notes.append('发布部门：' + flat(doc['publisher']))
    if notes:
        lines.append('【备注】' + '｜'.join(notes))

    lines.append('')
    lines.append(title)
    cite = [x for x in (subtitle, date) if x]
    if cite:
        lines.append('（' + '，'.join(cite) + '）')
    lines.append('')
    lines.append(doc['content'])
    return '\n'.join(lines) + '\n'


def dup_groups(docs):
    """找出「标题+文号」重名的组，用于试点样本覆盖去重后缀这条规则。"""
    seen = {}
    for doc in docs:
        key = (flat(doc.get('title')), flat(doc.get('subtitle')))
        seen.setdefault(key, []).append(doc)
    return [group for group in seen.values() if len(group) > 1]


def pick_pilot(docs, limit):
    """定向选样：刻意覆盖全部命名边界与各类字段缺失，不是随机抽。

    返回 [(doc, 选样理由)]，顺序即桶顺序，结果确定可复现。
    """
    def titled(doc):
        return flat(doc.get('title'))

    long_titles = [d for d in docs if len(('{}.txt'.format(titled(d))).encode('utf-8')) > NAME_MAX_BYTES]
    illegal = [d for d in docs if any(c in titled(d) for c in ILLEGAL_CHARS if c != '\x00')]
    no_subtitle = [d for d in docs if not flat(d.get('subtitle'))]
    by_len = sorted(docs, key=lambda d: -len(d.get('content') or ''))

    buckets = [
        ('边界·标题含非法字符', illegal[:2]),
        ('边界·标题超长需截断', long_titles[:2]),
        ('边界·无文号', no_subtitle[:2]),
        ('边界·正文超长', by_len[:2]),
    ]
    for group in dup_groups(docs)[:1]:
        buckets.append(('边界·重名需加序号', group[:2]))

    for aging in ('全文有效', '已修改'):
        buckets.append(('时效·' + aging, [d for d in docs if d.get('aging') == aging][:2]))
    buckets.append(('时效·空(=有效)', [d for d in docs if not d.get('aging')][:2]))

    buckets.append(('缺失·无税种', [d for d in docs if not d.get('taxLevel')][:1]))
    buckets.append(('缺失·无发布部门', [d for d in docs if not d.get('publisher')][:1]))

    # 每个 label 至少覆盖 2 条
    labels = []
    for doc in docs:
        if doc.get('label') and doc['label'] not in labels:
            labels.append(doc['label'])
    for label in labels:
        buckets.append(('覆盖·' + label,
                        [d for d in docs if d.get('label') == label][:2]))

    picked, seen = [], set()
    for reason, items in buckets:
        for doc in items:
            if len(picked) >= limit:
                return picked
            if doc['url'] in seen:
                continue
            seen.add(doc['url'])
            picked.append((doc, reason))
    return picked


def main():
    ap = argparse.ArgumentParser(description='国税总局政策法规库 → tigger_vault raw/')
    ap.add_argument('--jsonl', default=DEFAULT_JSONL, help='输入的 tax_policy.jsonl')
    ap.add_argument('--outdir', default=DEFAULT_OUTDIR, help='输出目录（相对 tigger_vault 仓库根）')
    ap.add_argument('--limit', type=int, default=0, help='只处理 N 条（0=全量）')
    ap.add_argument('--select', choices=['pilot', 'first'], default='pilot',
                    help='pilot=按边界定向选样；first=按文件顺序取前 N 条')
    ap.add_argument('--dry-run', action='store_true', help='只打印，不落盘')
    args = ap.parse_args()

    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    outdir = args.outdir if os.path.isabs(args.outdir) else os.path.join(repo_root, args.outdir)

    docs, dropped = [], {}
    for doc in load(args.jsonl):
        ok, why = keep(doc)
        if ok:
            docs.append(doc)
        else:
            dropped[why] = dropped.get(why, 0) + 1

    print('读入 {} 条；排除 {} 条：'.format(
        sum(dropped.values()) + len(docs), sum(dropped.values())))
    for why, count in sorted(dropped.items(), key=lambda x: -x[1]):
        print('    {:>5} 条  {}'.format(count, why))
    print('可入集合 {} 条'.format(len(docs)))

    names = assign_names(docs)      # 先给全部条目定名，试点才等于全量的预览

    if args.limit:
        if args.select == 'pilot':
            picked = pick_pilot(docs, args.limit)
        else:
            picked = [(d, '顺序') for d in docs[:args.limit]]
        print('\n本次取 {} 条：'.format(len(picked)))
    else:
        picked = [(d, '全量') for d in docs]

    if not args.dry_run:
        os.makedirs(outdir, exist_ok=True)

    taken, written = set(), []
    for doc, reason in picked:
        name = names[doc['url']]
        path = os.path.join(outdir, name)
        if args.dry_run:
            print('  [{}] {}\n        {}'.format(reason, name, flat(doc.get('title'))[:60]))
        else:
            with open(path, 'w', encoding='utf-8') as fp:
                fp.write(render(doc))
            written.append(path)

    if args.dry_run:
        print('\n--dry-run：没有写任何文件。加 --limit {} 去掉 --dry-run 即落盘。'.format(args.limit))
    else:
        print('\n已写入 {} 个文件到 {}'.format(len(written), outdir))
    return 0


if __name__ == '__main__':
    sys.exit(main())
