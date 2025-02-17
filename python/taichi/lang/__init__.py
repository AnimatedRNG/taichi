from .impl import *
from .matrix import Matrix

print = tprint
core = taichi_lang_core
runtime = pytaichi

i = indices(0)
j = indices(1)
k = indices(2)
l = indices(3)
ij = indices(0, 1)
ijk = indices(0, 1, 2)
Vector = Matrix
outer_product = Matrix.outer_product
cfg = default_cfg()
current_cfg = current_cfg()
x86_64 = core.x86_64
cuda = core.gpu
profiler_print = lambda: core.get_current_program().profiler_print()
profiler_clear = lambda: core.get_current_program().profiler_clear()

parallelize = core.parallelize
vectorize = core.vectorize
block_dim = core.block_dim
cache = core.cache
transposed = Matrix.transposed
polar_decompose = Matrix.polar_decompose
determinant = Matrix.determinant
set_default_fp = pytaichi.set_default_fp

def Tape(loss, clear_gradients=True):
  if clear_gradients:
    clear_all_gradients()
  loss[None] = 0
  loss.grad[None] = 1
  return runtime.get_tape(loss)

def clear_all_gradients():
  core.get_current_program().clear_all_gradients()

schedules = [parallelize, vectorize, block_dim, cache]
lang_core = core

__all__ = [s for s in dir() if not s.startswith('_')]

