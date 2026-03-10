import json
from collections.abc import Collection, Mapping
from pelican.urlwrappers import URLWrapper


def object_to_dict(x: object) -> dict[str, object] | None:
    if isinstance(x, URLWrapper):
        d = {}
        if x.name is not None:
            d['name'] = x.name
        if x.slug is not None:
            d['slug'] = x.slug
        return d
    else:
        try:
            d = vars(x)
        except TypeError:
            return None
        return {k: v for k, v in d.items() if k != 'settings' and not k.startswith('_')}


def tojson_helper(x: object, parts: list[str], ancestor_objs: set[object], depth: int, indentStr: str) -> None:
    if x is None:
        parts.append(json.dumps(x))
    elif isinstance(x, str):
        parts.append(json.dumps(x.strip()))
    elif isinstance(x, (int, float, bool)):
        parts.append(json.dumps(x))
    elif isinstance(x, Mapping):
        parts.append('{')
        if len(x) == 1:
            for k, v in x.items():
                if isinstance(k, (int, float, bool, str)):
                    parts.append(json.dumps(k))
                else:
                    raise TypeError('tojson: unknown key type ' + repr(type(k)))
                parts.append(': ')
                tojson_helper(v, parts, ancestor_objs, depth, indentStr)
        elif len(x) > 1:
            parts.append('\n')
            for i, (k, v) in enumerate(x.items()):
                parts.append(indentStr * (depth+1))
                if isinstance(k, (int, float, bool, str)):
                    parts.append(json.dumps(k))
                else:
                    raise TypeError('tojson: unknown key type ' + repr(type(k)))
                parts.append(': ')
                tojson_helper(v, parts, ancestor_objs, depth+1, indentStr)
                if i+1 < len(x):
                    parts.append(',\n')
            parts.append('\n')
            parts.append(indentStr * depth)
        parts.append('}')
    elif isinstance(x, Collection):
        parts.append('[')
        if len(x) == 1:
            for y in x:
                tojson_helper(y, parts, ancestor_objs, depth, indentStr)
        elif len(x) > 1:
            parts.append('\n')
            for i, y in enumerate(x):
                parts.append(indentStr * (depth+1))
                tojson_helper(y, parts, ancestor_objs, depth+1, indentStr)
                if i+1 < len(x):
                    parts.append(',\n')
            parts.append('\n')
            parts.append(indentStr * depth)
        parts.append(']')
    else:
        # print(type(x).__name__)
        parts.append(type(x).__name__)
        parts.append('(')
        if x in ancestor_objs:
            parts.append('…')
        else:
            ancestor_objs.add(x)
            tojson_helper(object_to_dict(x), parts, ancestor_objs, depth, indentStr)
            ancestor_objs.remove(x)
        parts.append(')')


def tojson(x: object) -> str:
    parts = []
    ancestor_objs = set()
    tojson_helper(x, parts, ancestor_objs, depth=0, indentStr='  ')
    return ''.join(parts)
