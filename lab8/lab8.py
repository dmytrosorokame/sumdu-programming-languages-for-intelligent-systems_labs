import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

OUT = 'screenshots'
os.makedirs(OUT, exist_ok=True)

# load data
data = np.genfromtxt('web_traffic.tsv', delimiter='\t')
x_raw = data[:, 0]
y_raw = data[:, 1]

print("=== 2.1 ===")
print(f"Shape: {data.shape}")
print(f"NaN count: {np.sum(np.isnan(y_raw))}")

mask = ~np.isnan(y_raw)
x = x_raw[mask]
y = y_raw[mask]
print(f"After cleanup: {len(x)} points")

# 2.2 scatter plot
plt.figure(figsize=(12, 6))
plt.scatter(x, y, s=10, alpha=0.5, label='Data')
plt.title('Web traffic: hits per hour')
plt.xlabel('Time (hours)')
plt.ylabel('Hits/hour')
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig(f'{OUT}/plot_2_2_scatter.png', dpi=150)
plt.close()
print("\n2.2 scatter saved")


def compute_error(y_true, y_pred):
    return np.sum((y_true - y_pred) ** 2)


# 2.3 degree 1
fp1 = np.polyfit(x, y, 1)
f1 = np.poly1d(fp1)

x_plot = np.linspace(x.min(), x.max(), 1000)

plt.figure(figsize=(12, 6))
plt.scatter(x, y, s=10, alpha=0.3, label='Data')
plt.plot(x_plot, f1(x_plot), 'r-', linewidth=2, label='Degree 1')
plt.title('Polynomial degree 1')
plt.xlabel('Time (hours)')
plt.ylabel('Hits/hour')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(f'{OUT}/plot_2_3_poly1.png', dpi=150)
plt.close()

error1 = compute_error(y, f1(x))
print(f"\n=== 2.3 ===")
print(f"Coefficients: {fp1}")
print(f"SSE: {error1:.2f}")

# 2.4 higher degree polynomials (variant 3: 5, 22, 42)
degrees = [2, 5, 22, 42]
colors = ['green', 'orange', 'purple', 'brown']
errors = {1: error1}

fig, axes = plt.subplots(2, 2, figsize=(16, 12))
axes = axes.ravel()

print(f"\n=== 2.4 ===")
for i, deg in enumerate(degrees):
    fp = np.polyfit(x, y, deg)
    f = np.poly1d(fp)
    y_pred = f(x_plot)
    err = compute_error(y, f(x))
    errors[deg] = err

    axes[i].scatter(x, y, s=5, alpha=0.3, label='Data')
    axes[i].plot(x_plot, y_pred, colors[i], linewidth=2, label=f'Degree {deg}')
    axes[i].set_title(f'Degree {deg} (SSE={err:.0f})')
    axes[i].set_xlabel('Time (hours)')
    axes[i].set_ylabel('Hits/hour')
    axes[i].legend()
    axes[i].grid(True, alpha=0.3)
    axes[i].set_ylim([0, max(y) * 1.5])

    print(f"  deg {deg}: SSE = {err:.2f}")

plt.suptitle('Polynomial approximation (variant 3)', fontsize=14)
plt.tight_layout()
plt.savefig(f'{OUT}/plot_2_4_polynomials.png', dpi=150)
plt.close()

print(f"\n  Error comparison:")
for deg in [1] + degrees:
    print(f"    deg {deg:2d}: SSE = {errors[deg]:.2f}")

# all polynomials on one plot
plt.figure(figsize=(14, 7))
plt.scatter(x, y, s=10, alpha=0.2, label='Data', color='gray')
plt.plot(x_plot, f1(x_plot), 'r-', linewidth=2, label=f'd=1 (SSE={errors[1]:.0f})')
for i, deg in enumerate(degrees):
    fp = np.polyfit(x, y, deg)
    f = np.poly1d(fp)
    plt.plot(x_plot, f(x_plot), colors[i], linewidth=2,
             label=f'd={deg} (SSE={errors[deg]:.0f})')
plt.ylim([0, max(y) * 1.5])
plt.title('All polynomials comparison')
plt.xlabel('Time (hours)')
plt.ylabel('Hits/hour')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(f'{OUT}/plot_2_4_all_polynomials.png', dpi=150)
plt.close()

# 2.5 inflection point + two lines
print(f"\n=== 2.5 ===")

best_error = np.inf
best_split = 0

for split_idx in range(50, len(x) - 50):
    split_val = x[split_idx]
    m1 = x <= split_val
    m2 = x > split_val

    if np.sum(m1) < 10 or np.sum(m2) < 10:
        continue

    fp_a = np.polyfit(x[m1], y[m1], 1)
    fp_b = np.polyfit(x[m2], y[m2], 1)

    err_a = compute_error(y[m1], np.polyval(fp_a, x[m1]))
    err_b = compute_error(y[m2], np.polyval(fp_b, x[m2]))
    total_err = err_a + err_b

    if total_err < best_error:
        best_error = total_err
        best_split = split_val

print(f"Inflection point: week {best_split:.0f}")
print(f"Two lines SSE: {best_error:.2f}")
print(f"Single line SSE: {errors[1]:.2f}")
print(f"Improvement: {(1 - best_error/errors[1])*100:.1f}%")

mask1 = x <= best_split
mask2 = x > best_split
fp_left = np.polyfit(x[mask1], y[mask1], 1)
fp_right = np.polyfit(x[mask2], y[mask2], 1)
f_left = np.poly1d(fp_left)
f_right = np.poly1d(fp_right)

x_left = np.linspace(x[mask1].min(), x[mask1].max(), 500)
x_right = np.linspace(x[mask2].min(), x[mask2].max(), 500)

plt.figure(figsize=(12, 6))
plt.scatter(x, y, s=10, alpha=0.3, label='Data', color='gray')
plt.plot(x_left, f_left(x_left), 'b-', linewidth=2, label=f'Line 1 (before {best_split:.0f})')
plt.plot(x_right, f_right(x_right), 'r-', linewidth=2, label=f'Line 2 (after {best_split:.0f})')
plt.axvline(x=best_split, color='k', linestyle='--', alpha=0.5, label=f'Split ({best_split:.0f})')
plt.title(f'Two-line fit (split at week {best_split:.0f})')
plt.xlabel('Time (hours)')
plt.ylabel('Hits/hour')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(f'{OUT}/plot_2_5_two_lines.png', dpi=150)
plt.close()

# 2.6 train/test split
print(f"\n=== 2.6 ===")

np.random.seed(42)
n = len(x)
indices = np.arange(n)
np.random.shuffle(indices)
split_point = int(n * 0.7)

train_idx = indices[:split_point]
test_idx = indices[split_point:]

x_train, y_train = x[train_idx], y[train_idx]
x_test, y_test = x[test_idx], y[test_idx]

print(f"Train: {len(x_train)}, Test: {len(x_test)}")

test_degrees = [1, 2, 5, 22, 42]
train_errors = {}
test_errors = {}

print(f"\n  {'deg':>8} | {'SSE train':>15} | {'SSE test':>15}")
print(f"  {'-'*8}-+-{'-'*15}-+-{'-'*15}")

for deg in test_degrees:
    fp = np.polyfit(x_train, y_train, deg)
    f = np.poly1d(fp)

    tr_err = compute_error(y_train, f(x_train))
    te_err = compute_error(y_test, f(x_test))
    train_errors[deg] = tr_err
    test_errors[deg] = te_err

    print(f"  {deg:>8} | {tr_err:>15.2f} | {te_err:>15.2f}")

fig, ax = plt.subplots(figsize=(10, 6))
x_pos = np.arange(len(test_degrees))
width = 0.35

ax.bar(x_pos - width/2, [train_errors[d] for d in test_degrees], width,
       label='Train', color='steelblue')
ax.bar(x_pos + width/2, [test_errors[d] for d in test_degrees], width,
       label='Test', color='coral')

ax.set_xlabel('Polynomial degree')
ax.set_ylabel('SSE')
ax.set_title('Train vs Test error')
ax.set_xticks(x_pos)
ax.set_xticklabels([str(d) for d in test_degrees])
ax.legend()
ax.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.savefig(f'{OUT}/plot_2_6_train_test.png', dpi=150)
plt.close()

fig, axes = plt.subplots(2, 3, figsize=(18, 10))
axes = axes.ravel()

for i, deg in enumerate(test_degrees):
    fp = np.polyfit(x_train, y_train, deg)
    f = np.poly1d(fp)

    axes[i].scatter(x_train, y_train, s=5, alpha=0.3, color='steelblue', label='Train')
    axes[i].scatter(x_test, y_test, s=5, alpha=0.3, color='coral', label='Test')
    axes[i].plot(x_plot, f(x_plot), 'k-', linewidth=2, label=f'd={deg}')
    axes[i].set_title(f'deg {deg}\nSSE train={train_errors[deg]:.0f}, test={test_errors[deg]:.0f}')
    axes[i].set_ylim([0, max(y) * 1.5])
    axes[i].legend(fontsize=8)
    axes[i].grid(True, alpha=0.3)

axes[5].axis('off')
plt.suptitle('Train set fit, test set evaluation', fontsize=14)
plt.tight_layout()
plt.savefig(f'{OUT}/plot_2_6_train_test_fits.png', dpi=150)
plt.close()

# 2.7 prediction: when will we hit 100k hits/hour?
print(f"\n=== 2.7 ===")

fp2_full = np.polyfit(x, y, 2)
f2_full = np.poly1d(fp2_full)
print(f"Degree 2: {fp2_full[0]:.6f}x^2 + {fp2_full[1]:.4f}x + {fp2_full[2]:.2f}")

target = 100000
coeffs = fp2_full.copy()
coeffs[2] -= target
roots = np.roots(coeffs)
real_positive_roots = [r.real for r in roots if np.isreal(r) and r.real > 0]

if real_positive_roots:
    prediction = min(real_positive_roots)
    print(f"100k hits/hour at week {prediction:.0f}")
    print(f"That's ~{prediction/52:.1f} years")
else:
    print("No solution found")
    prediction = None

target_linear = (target - fp_right[1]) / fp_right[0]
print(f"Linear extrapolation: week {target_linear:.0f}")

x_future = np.linspace(0, prediction * 1.1 if prediction else 2000, 2000)

plt.figure(figsize=(14, 7))
plt.scatter(x, y, s=10, alpha=0.3, label='Data', color='gray')
plt.plot(x_future, f2_full(x_future), 'r-', linewidth=2, label='Degree 2 fit')
plt.axhline(y=100000, color='g', linestyle='--', linewidth=1.5, label='Target: 100k')
if prediction:
    plt.axvline(x=prediction, color='purple', linestyle='--', alpha=0.7,
                label=f'Prediction: week {prediction:.0f}')
    plt.plot(prediction, 100000, 'r*', markersize=15, zorder=5)
plt.title('Prediction: 100,000 hits/hour')
plt.xlabel('Time (weeks)')
plt.ylabel('Hits/hour')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(f'{OUT}/plot_2_7_prediction.png', dpi=150)
plt.close()

print(f"\n{'='*50}")
print(f"SUMMARY")
print(f"{'='*50}")
print(f"Variant 3 (degrees: 5, 22, 42)")
print(f"Data points: {len(x)}")
print(f"\nSSE by degree:")
for deg in [1, 2, 5, 22, 42]:
    print(f"  deg {deg:2d}: {errors.get(deg, 'N/A')}")
print(f"\nInflection: week {best_split:.0f}")
print(f"Two-line SSE: {best_error:.2f}")
print(f"\n100k prediction:")
print(f"  Quadratic: week {prediction:.0f}" if prediction else "  N/A")
print(f"  Linear: week {target_linear:.0f}")
print(f"\nPlots saved to: {OUT}/")
