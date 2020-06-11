import numpy as np
import random
import math
import sys

OPT = 0

# add 0 to c & modify u_sum if it's not in c
def greedy_II(c, u_sum, B, verbose=False):
  n = len(c)
  eps = 1e-2
  max_tuple = (0, 0, 0)
  max_util = 0
  max_P = 0
  max_welfare = 0
  max_l = 0
  max_i = 0
  for i in range(n):
    if c[i] * i > B:
      continue
    eps_net = np.arange(0, 1 + eps, eps)
    for f in eps_net:
      l = i + 1
      if l == n:
        l = n - 1
      r = n - 1
      while l < r:
        m = int((l + r + 1) / 2)
        P = u_sum[i] * (c[i] + f * (c[m] - c[i])) + (u_sum[m] - u_sum[i]) * c[m] * f
        if P <= B:
          l = m
        else:
          r = m - 1
      P = u_sum[i] * (c[i] + f * (c[l] - c[i])) + (u_sum[l] - u_sum[i]) * c[l] * f
      if P > B:
        break
      util = u_sum[i] + f * (u_sum[min(l, n - 1)] - u_sum[i])
      if util > max_util:
        max_util = util
        max_tuple = (c[i], c[l], f)
        max_P = P
        max_l = l
        max_i = i
  if verbose == True:
    max_welfare = max_P
    for j in range(min(max_l, n - 1)):
      if j > 0 and j <= max_i:
        max_welfare = max_welfare - (u_sum[j] - u_sum[j - 1]) * c[j]
      elif j > max_i:
        max_welfare = max_welfare - max_tuple[2] * (u_sum[j] - u_sum[j - 1]) * c[j]
    print("Greedy_II utility: {0}, apx: {1}, expense: {2}, tuple: {3}, welfare: {4}, utilty/social cost: {5}".format(max_util, max_util / OPT, max_P, max_tuple, max_welfare, max_util / (max_P - max_welfare)))
  return (max_util, max_welfare, max_util / (max_P - max_welfare), max_tuple)

def random_sample_greedy(seller, B):
  delta = 1e-3
  B_half = (1-delta)*B/2
  B_left = B
  random_util = 0
  welfare = 0
  n = len(seller)
  random.shuffle(seller)
  parts = [seller[:int(n/2)], seller[int(n/2):], seller]
  dicts = [{0:0}, {0:0}, {0:0}]
  cs = [[],[],[]]
  u_sums = [[],[],[]]
  for k in range(3):
    parts[k].sort()
    for (c_i, u_i) in parts[k]:
      if c_i in dicts[k]:
        dicts[k][c_i] = dicts[k][c_i] + u_i
      else:
        dicts[k][c_i] = u_i
    for j, (c_j, u_j) in enumerate(dicts[k].items()):
      cs[k].append(c_j)
      if c_j == 0:
        u_sums[k].append(u_j)
      else:
        u_sums[k].append(u_j + u_sums[k][-1])
  (max_util1, max_welfare1, max_efficiency1, max_tuple1) = greedy_II(cs[0], u_sums[0], B_half)
  (max_util2, max_welfare2, max_efficiency2, max_tuple2) = greedy_II(cs[1], u_sums[1], B_half)
  (greedy_util, greedy_welfare, greedy_efficiency, max_tuple) = greedy_II(cs[2], u_sums[2], B, True)
  rules =[max_tuple1, max_tuple2]
  for k in range(2):
    (p1, p2, f) = rules[1-k]
    for (c_i, u_i) in parts[k]:
      if c_i <= p1 and (p1 + (p2 - p1) * f) * u_i <= B_left:
        B_left = B_left - (p1 + (p2 - p1) * f) * u_i
        random_util = random_util + u_i
        welfare = welfare + ((p1 + (p2 - p1) * f) * u_i - u_i * c_i)
      elif p1 < c_i and c_i <= p2 and p2 * f * u_i <= B_left:
        B_left = B_left - p2 * f * u_i
        random_util = random_util + f * u_i
        welfare = welfare + (p2 * f * u_i - f * u_i * c_i)
  print("RandomSample utility: {0}, apx: {1}, tuples: {2}, {3}, welfare: {4}, utility/social cost: {5}".format(random_util, random_util / OPT, max_tuple1, max_tuple2, welfare, random_util / (B - B_left - welfare)))
  return (greedy_util / OPT, greedy_welfare, greedy_efficiency, random_util / OPT, welfare, random_util / (B - B_left - welfare))

def AGN_I(seller, B):
  delta = 1e-3
  r = 0
  seller.sort()
  for s in seller:
    if s[0] != 0:
      r = s[0] / (math.e - 1)
      break
  AGN_util = 0
  AGN_B_used = 0
  AGN_r = 0
  AGN_welfare = 0
  while True:
    B_used = 0
    util = 0
    welfare = 0
    for s in seller:
      if (math.e-1) * r >= s[0]:
        B_used = B_used + s[1] * (r * math.e * math.log(math.e - s[0] / r) - r * (math.e - 1) + s[0])
        util = util + s[1] * math.log(math.e - s[0] / r)
        welfare = welfare + s[1] * (r * math.e * math.log(math.e - s[0] / r) - r * (math.e - 1) + s[0]) - s[1] * math.log(math.e - s[0] / r) * s[0]
    if B_used <= B:
      AGN_util = util
      AGN_r = r
      AGN_B_used = B_used
      AGN_welfare = welfare
      r = r * (1 + delta)
    else:
      break
  print("AGN_I utility: {0}, apx: {1}, expense: {2}, r: {3}, welfare: {4}, utilty/social cost: {5}".format(AGN_util, AGN_util / OPT, AGN_B_used, r, AGN_welfare, AGN_util / (AGN_B_used - AGN_welfare)))
  return (AGN_util / OPT, AGN_welfare, AGN_util / (AGN_B_used - AGN_welfare))

def cutoff(seller, B):
  seller.sort()
  n = len(seller)
  u_sum = []
  for i in range(n):
    if i == 0:
      u_sum.append(seller[i][1])
    else:
      u_sum.append(u_sum[i-1] + seller[i][1])
  l = 0
  r = n - 1
  while l < r:
    m = int((l + r + 1) / 2)
    if seller[m][0] * u_sum[m] > B:
      r = m - 1
    else:
      l = m
  welfare = seller[l][0] * u_sum[l]
  for i in range(l+1):
    welfare = welfare - seller[i][0] * seller[i][1]
  print("cutoff utility: {0}, apx: {1}, expense: {2}, welfare: {3}, utilty/social cost: {4}".format(u_sum[l], u_sum[l] / OPT, seller[l][0] * u_sum[l], welfare, u_sum[l]/(seller[l][0] * u_sum[l] - welfare)))
  return (u_sum[l] / OPT, welfare, u_sum[l]/(seller[l][0] * u_sum[l] - welfare))

def run1():
  sys.stdout = open('log_table_1_2_3.txt', 'w')
  f = open("output_table_1_2_3.txt", "a")
  T = 100
  B = 20000
  global B_global
  B_global = B
  for distribution in range(5):
    mean_util = [0, 0, 0, 0]
    std_util = [0, 0, 0, 0]
    mean_welfare = [0, 0, 0, 0]
    std_welfare = [0, 0, 0, 0]
    mean_efficiency = [0, 0, 0, 0]
    std_efficiency = [0, 0, 0, 0]
    for time in range(T):
      seller = []
      for i in range(1000):
        c = 0
        if distribution == 0:
          c = np.random.normal(20, 5)
        elif distribution == 1:
          c = np.random.uniform(0,40)
        elif distribution == 2:
          c = np.random.exponential(20)
        elif distribution == 3:
          coin = np.random.randint(2)
          if coin == 0:
            c = np.random.normal(30, 3)
          else:
            c = np.random.normal(10, 3)
        elif distribution == 4:
          coin = np.random.randint(3)
          if coin == 0:
            c = np.random.normal(35, 3)
          elif coin == 1:
            c = np.random.normal(20, 3)
          elif coin == 2:
            c = np.random.normal(5, 3)
        c = max(c, 0)
        seller.append((c, 1))
      seller_tmp = seller.copy()
      seller_tmp.sort()
      B_used = 0
      global OPT
      OPT = 0
      for s in seller_tmp:
        if B_used + s[0]*s[1] <= B:
          OPT = OPT + s[1]
          B_used = B_used + s[0]*s[1]
        else:
          OPT = OPT + ((B - B_used) / s[0]) * s[1]
          B_used = B
          break
      print("distribution: {0}, OPT utillity: {1}".format(distribution, OPT))
      (apx_cutoff, welfare_cutoff, efficiency_cutoff) = cutoff(seller, B)
      (apx_agn, welfare_agn, efficiency_agn) = AGN_I(seller, B)
      (apx_greedy, welfare_greedy, efficiency_greedy, apx_random, welfare_random, efficiency_random) = random_sample_greedy(seller, B)

      mean_util[0] = (mean_util[0] * time + apx_cutoff) * 1.0 / (time + 1)
      mean_util[1] = (mean_util[1] * time + apx_agn) * 1.0 / (time + 1)
      mean_util[2] = (mean_util[2] * time + apx_greedy) * 1.0 / (time + 1)
      mean_util[3] = (mean_util[3] * time + apx_random) * 1.0 / (time + 1)

      std_util[0] = (std_util[0] * time + apx_cutoff**2) * 1.0 / (time + 1)
      std_util[1] = (std_util[1] * time + apx_agn**2) * 1.0 / (time + 1)
      std_util[2] = (std_util[2] * time + apx_greedy**2) * 1.0 / (time + 1)
      std_util[3] = (std_util[3] * time + apx_random**2) * 1.0 / (time + 1)
     
      mean_welfare[0] = (mean_welfare[0] * time + welfare_cutoff) * 1.0 / (time + 1)
      mean_welfare[1] = (mean_welfare[1] * time + welfare_agn) * 1.0 / (time + 1)
      mean_welfare[2] = (mean_welfare[2] * time + welfare_greedy) * 1.0 / (time + 1)
      mean_welfare[3] = (mean_welfare[3] * time + welfare_random) * 1.0 / (time + 1)

      std_welfare[0] = (std_welfare[0] * time + welfare_cutoff**2) * 1.0 / (time + 1)
      std_welfare[1] = (std_welfare[1] * time + welfare_agn**2) * 1.0 / (time + 1)
      std_welfare[2] = (std_welfare[2] * time + welfare_greedy**2) * 1.0 / (time + 1)
      std_welfare[3] = (std_welfare[3] * time + welfare_random**2) * 1.0 / (time + 1)

      mean_efficiency[0] = (mean_efficiency[0] * time + efficiency_cutoff) * 1.0 / (time + 1)
      mean_efficiency[1] = (mean_efficiency[1] * time + efficiency_agn) * 1.0 / (time + 1)
      mean_efficiency[2] = (mean_efficiency[2] * time + efficiency_greedy) * 1.0 / (time + 1)
      mean_efficiency[3] = (mean_efficiency[3] * time + efficiency_random) * 1.0 / (time + 1)

      std_efficiency[0] = (std_efficiency[0] * time + efficiency_cutoff**2) * 1.0 / (time + 1)
      std_efficiency[1] = (std_efficiency[1] * time + efficiency_agn**2) * 1.0 / (time + 1)
      std_efficiency[2] = (std_efficiency[2] * time + efficiency_greedy**2) * 1.0 / (time + 1)
      std_efficiency[3] = (std_efficiency[3] * time + efficiency_random**2) * 1.0 / (time + 1)
   
    for mech in range(4):
      std_util[mech] = math.sqrt((std_util[mech] - mean_util[mech]**2) * 1.0 * T / (T-1))
    for mech in range(4):
      std_welfare[mech] = math.sqrt((std_welfare[mech] - mean_welfare[mech]**2) * 1.0 * T / (T-1))
    for mech in range(4):
      std_efficiency[mech] = math.sqrt((std_efficiency[mech] - mean_efficiency[mech]**2) * 1.0 * T / (T-1))

    print("distribution: {0}, mean_apx_cutoff: {1}, std_apx_cutoff: {2}, mean_apx_agn: {3}, std_apx_agn: {4}, mean_apx_greedy: {5}, std_apx_greedy: {6}, mean_apx_random: {7}, std_apx_random: {8}".format(distribution, mean_util[0], std_util[0], mean_util[1], std_util[1], mean_util[2], std_util[2], mean_util[3], std_util[3]), file=f)
    print("distribution: {0}, mean_welfare_cutoff: {1}, std_welfare_cutoff: {2}, mean_welfare_agn: {3}, std_welfare_agn: {4}, mean_welfare_greedy: {5}, std_welfare_greedy: {6}, mean_welfare_random: {7}, std_welfare_random: {8}".format(distribution, mean_welfare[0], std_welfare[0], mean_welfare[1], std_welfare[1], mean_welfare[2], std_welfare[2], mean_welfare[3], std_welfare[3]), file=f)
    print("distribution: {0}, mean_efficiency_cutoff: {1}, std_efficiency_cutoff: {2}, mean_efficiency_agn: {3}, std_efficiency_agn: {4}, mean_efficiency_greedy: {5}, std_efficiency_greedy: {6}, mean_efficiency_random: {7}, std_efficiency_random: {8}".format(distribution, mean_efficiency[0], std_efficiency[0], mean_efficiency[1], std_efficiency[1], mean_efficiency[2], std_efficiency[2], mean_efficiency[3], std_efficiency[3]), file=f)
  f.close()

def run2():
  sys.stdout = open('log_figure_2.txt', 'w')
  f = open("output_figure_2.txt", "a")
  T = 20

  for n in [100, 300, 1000, 3000, 10000]:
    B = n * 20
    global B_global
    B_global = B
    for distribution in range(3):
      mean_util_diff = 0
      std_util_diff = 0
      mean_util = [0,0]
      std_util = [0,0]
      for time in range(T):
        seller = []
        for i in range(n):
          c = 0
          if distribution == 0:
            c = np.random.normal(20, 5)
          elif distribution == 1:
            c = np.random.uniform(0,40)
          elif distribution == 2:
            c = np.random.exponential(20)
          c = max(c, 0)
          seller.append((c, 1))
        seller_tmp = seller.copy()
        seller_tmp.sort()
        B_used = 0
        global OPT
        OPT = 0
        for s in seller_tmp:
          if B_used + s[0]*s[1] <= B:
            OPT = OPT + s[1]
            B_used = B_used + s[0]*s[1]
          else:
            OPT = OPT + ((B - B_used) / s[0]) * s[1]
            B_used = B
            break
        (apx_greedy, welfare_greedy, efficiency_greedy, apx_random, welfare_random, efficiency_random) = random_sample_greedy(seller, B)
        mean_util_diff = (mean_util_diff * time + (apx_greedy - apx_random)) * 1.0 / (time + 1)
        std_util_diff = (std_util_diff * time + (apx_greedy - apx_random)**2) * 1.0 / (time + 1)
        mean_util[0] = (mean_util[0] * time + apx_greedy) * 1.0 / (time + 1)
        mean_util[1] = (mean_util[1] * time + apx_random) * 1.0 / (time + 1)
        std_util[0] = (std_util[0] * time + apx_greedy**2) * 1.0 / (time + 1)
        std_util[1] = (std_util[1] * time + apx_random**2) * 1.0 / (time + 1)

      std_util_diff = math.sqrt(std_util_diff - mean_util_diff**2)
      std_util[0] = math.sqrt(std_util[0] - mean_util[0]**2)
      std_util[1] = math.sqrt(std_util[1] - mean_util[1]**2)
      print("distribution: {0}, mean diff: {1}, std diff: {2}, mean apx greedy: {3}, std apx greedy: {4}, mean apx random: {5}, std apx random: {6}, number of sellers: {7}".format(distribution, mean_util_diff, std_util_diff, mean_util[0], std_util[0], mean_util[1], std_util[1], n), file=f)

if sys.argv[1] == '1':
  run1()
else:
  run2()