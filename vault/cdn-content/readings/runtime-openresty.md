---
nodes: [runtimes.lua-openresty]
url: https://github.com/openresty/lua-nginx-module#readme
tags: [canonical]
---
# OpenResty `lua-nginx-module` reference

The project's canonical reference for Nginx request phases, cosockets, Lua VM lifetime, and shared dictionaries—the runtime facts that determine whether edge Lua stays nonblocking.

**Extract on read:**
- Which APIs and yielding behavior are legal in each request phase.
- Why blocking foreign socket libraries stall an Nginx worker.
- What module globals and `ngx.shared.DICT` do and do not share.

%% trellis:begin %%
## Source
[Open the original ↗](https://github.com/openresty/lua-nginx-module#readme)
%% trellis:end %%
