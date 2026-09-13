"""Tree-walking renderer for minimako's AST, dispatched by the Visitor pattern: `visit()` looks
up `visit_<NodeClassName>` and calls it. Every node type defined in `ast.py` needs a matching
`visit_*` method here -- if one is missing, `visit()` raises `AttributeError`.
"""

from __future__ import annotations

from . import ast as astmod


class Compiler:
    """One Compiler per render call, or per nested scope: a visitor that needs an isolated
    context (e.g. loop body, included template) constructs its own child Compiler so that
    scope's bindings don't leak into the caller."""

    def __init__(self, context: dict, current_template=None):
        self.context = context
        self.current_template = current_template

    def render(self, node: astmod.Node) -> str:
        return self.visit(node)

    def visit(self, node: astmod.Node) -> str:
        method_name = f"visit_{type(node).__name__}"
        visitor = getattr(self, method_name, None)
        if visitor is None:
            raise AttributeError(
                f"Compiler has no visitor for node type {type(node).__name__!r} "
                f"(expected a method named {method_name!r})"
            )
        return visitor(node)

    def visit_TemplateNode(self, node: astmod.TemplateNode) -> str:
        return "".join(self.visit(child) for child in node.body)

    def visit_TextNode(self, node: astmod.TextNode) -> str:
        return node.text

    def visit_ExpressionNode(self, node: astmod.ExpressionNode) -> str:
        value = eval(node.expr, {"__builtins__": {}}, self.context)  # noqa: S307 - sandboxed
        return str(value)

    def visit_IfNode(self, node: astmod.IfNode) -> str:
        if eval(node.cond, {"__builtins__": {}}, self.context):  # noqa: S307 - sandboxed
            return "".join(self.visit(child) for child in node.body)
        return ""

    def visit_ForNode(self, node: astmod.ForNode) -> str:
        iterable = eval(node.iter_expr, {"__builtins__": {}}, self.context)  # noqa: S307
        out = []
        for item in iterable:
            loop_context = dict(self.context)
            loop_context[node.target] = item
            child = Compiler(loop_context, self.current_template)
            out.append("".join(child.visit(n) for n in node.body))
        return "".join(out)
