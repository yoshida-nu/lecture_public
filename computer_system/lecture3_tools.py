# -*- coding: utf-8 -*-
# 同じ元波形に対して fs（サンプリング周波数）と bits（量子化ビット数）を変え，
# 波形（グラフ）＋聴こえ方（WAV保存）を体験する．

import os
import platform
import wave
import numpy as np
import matplotlib.pyplot as plt
import subprocess


# -----------------------------
# 1) 元の音（基準信号）を作る
# -----------------------------
def make_base_signal(fs_base: int = 44100, duration_sec: float = 2.0) -> np.ndarray:
    t = np.arange(int(fs_base * duration_sec), dtype=np.float32) / fs_base

    # 単調すぎないように複数成分＋弱い振幅変調
    x = (
        0.55 * np.sin(2 * np.pi * 440 * t) +
        0.20 * np.sin(2 * np.pi * 880 * t) +
        0.12 * np.sin(2 * np.pi * 1760 * t) +
        0.08 * np.sin(2 * np.pi * 3000 * t)
    )
    x *= (0.65 + 0.35 * np.sin(2 * np.pi * 2.0 * t))

    # 余裕を持たせて正規化
    x = x / (np.max(np.abs(x)) + 1e-12) * 0.95
    return x.astype(np.float32)


# ---------------------------------------
# 2) リサンプリング（SciPyなし：線形補間）
# ---------------------------------------
def resample_linear(x: np.ndarray, fs_in: int, fs_out: int) -> np.ndarray:
    if fs_in == fs_out:
        return x.astype(np.float32, copy=True)

    duration = len(x) / fs_in
    n_out = int(round(duration * fs_out))

    t_in = np.arange(len(x), dtype=np.float64) / fs_in
    t_out = np.arange(n_out, dtype=np.float64) / fs_out

    y = np.interp(t_out, t_in, x).astype(np.float32)
    return y


# -----------------------------
# 3) 量子化（bits bit 相当）
# -----------------------------
def quantize_pcm(x: np.ndarray, bits: int) -> np.ndarray:
    x = np.asarray(x, dtype=np.float32)
    x = np.clip(x, -1.0, 1.0)

    if bits < 2:
        raise ValueError("bits は 2 以上を指定してください．")

    max_int = (1 << (bits - 1)) - 1
    min_int = -(1 << (bits - 1))

    q = np.round(x * max_int).astype(np.int64)
    q = np.clip(q, min_int, max_int)

    y = (q / max_int).astype(np.float32)
    return y


# --------------------------------
# 4) WAV保存（標準ライブラリ wave）
# --------------------------------
def write_wav_mono_int16(filename: str, x: np.ndarray, fs: int) -> None:
    x = np.asarray(x, dtype=np.float32)
    x = np.clip(x, -1.0, 1.0)

    data = (x * 32767.0).astype(np.int16)

    with wave.open(filename, "wb") as wf:
        wf.setnchannels(1)      # mono
        wf.setsampwidth(2)      # int16
        wf.setframerate(fs)
        wf.writeframes(data.tobytes())


# -----------------------------
# 5) 波形比較プロット
# -----------------------------
def plot_waveforms(x_base: np.ndarray, fs_base: int,
                   x_proc: np.ndarray, fs_proc: int,
                   title: str,
                   zoom_ms: float = 6.0) -> None:
    n_base = int(fs_base * (zoom_ms / 1000.0))
    n_proc = int(fs_proc * (zoom_ms / 1000.0))

    n_base = min(n_base, len(x_base))
    n_proc = min(n_proc, len(x_proc))

    t_base = (np.arange(n_base) / fs_base) * 1000.0
    t_proc = (np.arange(n_proc) / fs_proc) * 1000.0

    plt.figure(figsize=(10, 4))
    plt.plot(t_base, x_base[:n_base], linewidth=1.0, label=f"Original (fs={fs_base} Hz)")
    plt.plot(t_proc, x_proc[:n_proc], linewidth=1.0, label=f"Processed (fs={fs_proc} Hz)")
    plt.title(title)
    plt.xlabel("Time [ms]")
    plt.ylabel("Amplitude")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()


# -----------------------------
# 6) 実験本体：グラフ＋WAV保存
# -----------------------------
def run_experiment(fs_list, bits_list,
                   fs_base: int = 44100,
                   duration_sec: float = 2.0,
                   zoom_ms: float = 6.0,
                   normalize_each: bool = False,
                   out_dir: str = "out_wav") -> None:
    os.makedirs(out_dir, exist_ok=True)

    x_base = make_base_signal(fs_base=fs_base, duration_sec=duration_sec)

    # 基準音を保存・再生
    base_path = os.path.join(out_dir, f"base_fs{fs_base}.wav")
    write_wav_mono_int16(base_path, x_base, fs_base)


    for fs in fs_list:
        x_fs = resample_linear(x_base, fs_in=fs_base, fs_out=fs)

        for bits in bits_list:
            x_q = quantize_pcm(x_fs, bits=bits)

            x_play = x_q.copy()
            if normalize_each:
                m = np.max(np.abs(x_play)) + 1e-12
                x_play = x_play / m * 0.95

            title = f"fs={fs} Hz, {bits}-bit Quantization (Zoom: {zoom_ms} ms)"
            plot_waveforms(x_base, fs_base, x_q, fs, title=title, zoom_ms=zoom_ms)

            path = os.path.join(out_dir, f"sound_fs{fs}_bits{bits}.wav")
            write_wav_mono_int16(path, x_play, fs)

            