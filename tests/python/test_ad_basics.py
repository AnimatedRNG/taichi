import taichi as ti
from pytest import approx
import math
import autograd.numpy as np
from autograd import grad

def grad_test(tifunc, npfunc=None):
  if npfunc is None:
    npfunc = tifunc
  ti.reset()

  x = ti.var(ti.f32)
  y = ti.var(ti.f32)

  @ti.layout
  def place():
    ti.root.dense(ti.i, 1).place(x, x.grad, y, y.grad)

  @ti.kernel
  def func():
    for i in x:
      y[i] = tifunc(x[i])

  v = 0.2

  y.grad[0] = 1
  x[0] = v
  func()
  func.grad()

  assert y[0] == approx(npfunc(v))
  assert x.grad[0] == approx(grad(npfunc)(v))

def test_size1():
  ti.reset()
  x = ti.var(ti.i32)

  @ti.layout
  def place():
    ti.root.dense(ti.i, 1).place(x)

  x[0] = 1
  assert x[0] == 1

def test_poly():
  grad_test(lambda x: x)
  grad_test(lambda x: -x)
  grad_test(lambda x: x * x)
  grad_test(lambda x: ti.sqr(x))
  grad_test(lambda x: x * x * x)
  grad_test(lambda x: x * x * x * x)
  grad_test(lambda x: 0.4 * x * x - 3)
  grad_test(lambda x: (x - 3) * (x - 1))
  grad_test(lambda x: (x - 3) * (x - 1) + x * x)

def test_trigonometric():
  grad_test(lambda x: ti.sin(x), lambda x: np.sin(x))
  grad_test(lambda x: ti.cos(x), lambda x: np.cos(x))
  grad_test(lambda x: ti.tanh(x), lambda x: np.tanh(x))

def test_frac():
  grad_test(lambda x: 1 / x)
  grad_test(lambda x: (x + 1) / (x - 1))
  grad_test(
    lambda x: (x + 1) * (x + 2) / ((x - 1) * (x + 3)))

def test_unary():
  grad_test(lambda x: ti.sqrt(x), lambda x: np.sqrt(x))
  grad_test(lambda x: ti.exp(x), lambda x: np.exp(x))
  grad_test(lambda x: ti.log(x), lambda x: np.log(x))

def test_minmax():
  grad_test(lambda x: ti.min(x, 0), lambda x: np.minimum(x, 0))
  grad_test(lambda x: ti.min(x, 1), lambda x: np.minimum(x, 1))
  grad_test(lambda x: ti.min(0, x), lambda x: np.minimum(0, x))
  grad_test(lambda x: ti.min(1, x), lambda x: np.minimum(1, x))
  
  grad_test(lambda x: ti.max(x, 0), lambda x: np.maximum(x, 0))
  grad_test(lambda x: ti.max(x, 1), lambda x: np.maximum(x, 1))
  grad_test(lambda x: ti.max(0, x), lambda x: np.maximum(0, x))
  grad_test(lambda x: ti.max(1, x), lambda x: np.maximum(1, x))

