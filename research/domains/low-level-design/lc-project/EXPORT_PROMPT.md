Export the LeetCode Project workspace files for the project `{SLUG}`. Chi (the account owner, Premium, 100 practice
starts a day) asked for every project's full workspace on his machine. Never submit anything. Never print a token.
Always `await` promises in javascript_tool.

Tools: load with ToolSearch first: select_browser, tabs_context_mcp, tabs_create_mcp, navigate, javascript_tool,
computer, read_page, find, tabs_close_mcp.

1. Browser: call tabs_context_mcp. If it asks for a browser, call select_browser with the connected browser marked
   local (this Mac); its deviceId was 485dfb23-82b2-4ee8-8230-f47b715fca25. Never pick a non-local browser.
2. Open a NEW tab at https://leetcode.com/project/?detail={SLUG} and wait for it to load.
3. Start (or reuse) the practice in Python with javascript_tool:
   const q=(query,variables)=>fetch("/graphql/",{method:"POST",headers:{"content-type":"application/json","x-csrftoken":(document.cookie.match(/csrftoken=([^;]+)/)||[])[1]||""},body:JSON.stringify({query,variables})}).then(r=>r.json());
   const cur=await q("query($s:String){ projectPracticeSession(problemSlug:$s){ id status runtimeKey } }",{s:"{SLUG}"});
   let out={current:cur.data&&cur.data.projectPracticeSession};
   if(!out.current||!["PREPARING","RUNNING","READY","ACTIVE"].includes(out.current.status)){const s=await q("mutation($s:String!,$r:String){ startProjectPractice(problemSlug:$s, runtimeKey:$r){ ok error errorCode quota{ remaining } session{ id status } } }",{s:"{SLUG}",r:"python-3.11"}); out.start=s.data&&s.data.startProjectPractice;}
   JSON.stringify(out)
   If start fails with an error saying another practice is active, end that other one only if it is a LeetCode Project
   practice (mutation endProjectPractice(problemSlug) for its slug), then retry once.
4. Navigate the tab to https://leetcode.com/project/{SLUG}/ and wait until the Theia workspace inside the iframe has
   loaded and its "Task: Setup" has finished or at least the Explorer shows files (screenshots; up to 3 minutes).
5. In the Explorer expand every folder except venv, .venv, node_modules, __pycache__, .git, .pytest_cache. Record every
   file path you see (folders expanded). Take a screenshot of the whole expanded tree.
6. Select every top-level item except venv, .venv, node_modules, __pycache__, .git, .pytest_cache (click the first,
   shift-click the last, cmd-click to deselect the excluded ones), right-click the selection, choose "Download". Wait 15
   seconds.
7. End the practice: run with javascript_tool on the leetcode.com page
   JSON.stringify(await (await fetch("/graphql/",{method:"POST",headers:{"content-type":"application/json","x-csrftoken":(document.cookie.match(/csrftoken=([^;]+)/)||[])[1]||""},body:JSON.stringify({query:"mutation($s:String!){ endProjectPractice(problemSlug:$s){ ok error errorCode } }",variables:{s:"{SLUG}"}})})).json())
8. Close the tab you opened.

Reply in exactly this form:
SLUG: {SLUG}
START: <the JSON from step 3>
FILES:
<one path per line, every file in the expanded tree, with a trailing / for folders and (locked) where a lock icon shows>
DOWNLOAD: <done / what blocked it>
END: <the JSON from step 7>
NOTES: <anything unusual: extra panes, setup errors, files you could not expand>
