import numpy as np

def update1d(mean1, var1, mean2, var2):
  new_mean = (var2 * mean1 + var1 * mean2) / (var1 + var2)
  new_var = 1 / (1 / var1 + 1 / var2)
  return new_mean, new_var

def predict1d(mean1, var1, mean2, var2):
  new_mean = mean1 + mean2
  new_var = var1 + var2
  return new_mean, new_var


def test1d():
  # measurement uncertainty
  measurement_sig = 4
  # motion uncertainty
  motion_sig = 2

  mu = 0
  sig = 10000

  # test values
  measurements = [5, 6, 7, 9, 10]
  motions = [1, 1, 2, 1, 1]
  for i in range(len(measurements)):
    mu, sig = update1d(mu, sig, measurements[i], measurement_sig)
    print("update: ", mu, sig)
    mu, sig = predict1d(mu, sig, motions[i], motion_sig)
    print("predict: ", mu, sig)

def filter(x, P, u, F, H, R, I, measurements):

  for measurement in measurements:
    x = np.matmul(F, x) + u
    P = np.matmul(np.matmul(F, P), np.transpose(F))

    Z = np.array([measurement])
    y = np.transpose(Z) - np.matmul(H, x)
    S = np.matmul(np.matmul(H, P), np.transpose(H)) + R
    K = np.matmul(np.matmul(P, np.transpose(H)), np.linalg.inv(S))
    x = x + np.matmul(K, y)
    P = np.matmul(I - np.matmul(K, H), P)

  print(x)
  print("---")
  print(P)

def test2d():
  measurements = [1,2,3]

  x = np.array([[0.], [0.]]) # initial state (location and velocity)
  P = np.array([[1000., 0.], [0., 1000.]]) # initial uncertainty
  u = np.array([[0.], [0.]]) # external motion
  F = np.array([[1., 1.], [0, 1.]]) # next state function
  H = np.array([[1., 0.]]) # measurement function
  R = np.array([[1.]]) # measurement uncertainty
  I = np.array([[1., 0.], [0., 1.]]) # identity matrix

  filter(x, P, u, F, H, R, I, measurements)

def test4d():
  measurements = [ 
    [5., 10.],
    [6., 8.],
    [7., 6.],
    [8., 4.],
    [9., 2.],
    [10., 0.] ]
  initial_xy = [4., 12.]

  # measurements = [[1., 4.], [6., 0.], [11., -4.], [16., -8.]]
  # initial_xy = [-4., 8.]

  # measurements = [[1., 17.], [1., 15.], [1., 13.], [1., 11.]]
  # initial_xy = [1., 19.]

  dt = 0.1

  # initial state (location and velocity)
  x = np.array(
    [ [initial_xy[0]],
      [initial_xy[1]],
      [0.],
      [0.] ] )

  # external motion
  u = np.array(
    [ [0.],
      [0.],
      [0.],
      [0.] ] )

  # initial uncertainty: 0 for positions x and y, 1000 for the two velocities
  P =  np.array(
    [ [0., 0., 0., 0.],
      [0., 0., 0., 0.],
      [0., 0., 1000., 0.],
      [0., 0., 0., 1000.] ])
  # next state function: generalize the 2d version to 4d
  F =  np.array(
    [ [1., 0., dt, 0.],
      [0., 1., 0., dt],
      [0., 0., 1., 0.],
      [0., 0., 0., 1.] ])
  # measurement function: reflect the fact that we observe x and y but not the two velocities
  H =  np.array(
    [ [1., 0., 0., 0.],
      [0., 1., 0., 0.] ])
  # measurement uncertainty: use 2x2 matrix with 0.1 as main diagonal
  R =  np.array(
    [ [0.1, 0.],
      [0., 0.1] ])
  # 4d identity matrix
  I =  np.array(
    [ [1., 0., 0., 0.],
      [0., 1., 0., 0.],
      [0., 0., 1., 0.],
      [0., 0., 0., 1.] ])

  filter(x, P, u, F, H, R, I, measurements)


if __name__ == "__main__":
  # print("test2d")
  # test2d()

  # print("test4d")
  test4d()
