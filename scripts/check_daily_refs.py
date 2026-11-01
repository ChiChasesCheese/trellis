"""Check the LC numbers and names in the 同模式 line of every daily card against LeetCode (prints only mismatches)."""
import re,glob,json,urllib.request
meta=json.load(open("research/companies/tiktok/catalog/lc_meta.json"))
def lookup(n):
    if str(n) in meta: return meta[str(n)]["zh"]
    q='query($k:String!){problemsetQuestionList(categorySlug:"",limit:5,skip:0,filters:{searchKeywords:$k}){questions{frontendQuestionId title titleCn}}}'
    req=urllib.request.Request("https://leetcode.cn/graphql/",data=json.dumps({"query":q,"variables":{"k":str(n)}}).encode(),headers={"Content-Type":"application/json","Referer":"https://leetcode.cn","User-Agent":"curl/8.7.1"})
    try:
        for x in json.load(urllib.request.urlopen(req,timeout=20))["data"]["problemsetQuestionList"]["questions"]:
            if x["frontendQuestionId"]==str(n): return x["titleCn"] or x["title"]
    except Exception as e: return f"?{e}"
    return "?"
for f in sorted(glob.glob("vault/interviews/core/leetcode/daily/cards/*/*.md")):
    t=open(f).read()
    m=re.search(r"\*\*同模式。\*\*(.*)",t)
    if not m: print("NO 同模式",f); continue
    core=re.search(r"\*\*核心题。\*\*\n\n((?:- .*\n?)+)",t)
    if not core: print("NO 核心题",f)
    refs=m.group(1)+"、"+(core.group(1) if core else "")
    for n,name in re.findall(r"LC (\d+) ([^、，。（(：\n]+)",refs):
        real=lookup(int(n))
        norm=lambda x: re.sub(r"[\s「」“”\"'·]","",x or "")
        ok = real and (norm(name)[:3] in norm(real) or norm(real)[:3] in norm(name))
        if not ok: print(f.split("tlc-daily-")[1][:40], "| card:",n,name.strip(),"| real:",real)
