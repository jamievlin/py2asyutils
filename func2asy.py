#!/usr/bin/env python3

import typing as t
import numpy as np

def func2asy(funcname: str, func: t.Callable[[float], float], from_a: float=0.0, from_b: float=1.0, detail: int=100, realtype:str='realfunc') -> str:
    sample = int(detail * (from_b - from_a))

    basearray = np.linspace(from_a, from_b, sample)
    yarray = func(basearray)

    return '{0} {1}=fspline({2},{3});'.format(realtype, funcname, arr2asyarr(basearray), arr2asyarr(yarray))

def arr2asyarr(arr, typ: str='real'):
    return 'new {1:s}[] {{{0:s}}}'.format(','.join([str(val) for val in arr]), typ)
