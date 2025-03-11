import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import subprocess

# Get the SYN packets
subprocess.run(
    "tshark -r syn_flood.pcap -Y 'tcp.flags.syn==1' -T fields -e frame.time_epoch -e ip.src -e ip.dst -e tcp.srcport -e tcp.dstport > syn_connections.txt",
    shell=True,
)

# Get the FIN and RST packets
subprocess.run(
    "tshark -r syn_flood.pcap -Y 'tcp.flags.fin==1 || tcp.flags.reset==1' -T fields -e frame.time_epoch -e ip.src -e ip.dst -e tcp.srcport -e tcp.dstport > connection_end.txt",
    shell=True,
)

syn_df = pd.read_csv(
    "syn_connections_mitigated.txt",
    delimiter="\t",
    names=["time", "src_ip", "dst_ip", "src_port", "dst_port"],
    dtype={"time": float},
)

fin_rst_df = pd.read_csv(
    "connection_end_mitigated.txt",
    delimiter="\t",
    names=["time", "src_ip", "dst_ip", "src_port", "dst_port"],
    dtype={"time": float},
)


start_time = syn_df["time"].min()
syn_df["time"] -= start_time
fin_rst_df["time"] -= start_time

# Added tqdm for progress bar (as pcap file is large)
connections = {}
for _, row in tqdm(syn_df.iterrows(), total=len(syn_df), desc="Processing SYN packets"):
    key = (row["src_ip"], row["dst_ip"], row["src_port"], row["dst_port"])
    connections[key] = row["time"]

durations = []
for _, row in tqdm(
    fin_rst_df.iterrows(), total=len(fin_rst_df), desc="Processing FIN/RST packets"
):
    key = (row["src_ip"], row["dst_ip"], row["src_port"], row["dst_port"])
    if key in connections:
        duration = row["time"] - connections[key]
        if duration >= 0:
            durations.append((connections[key], duration))
        del connections[key]
    else:
        durations.append((row["time"], 100))

for key, syn_time in connections.items():
    durations.append((syn_time, 100))

df_duration = pd.DataFrame(durations, columns=["start_time", "duration"])

df_duration["color"] = np.where(df_duration["duration"] == 100, "red", "blue")

# Plot
plt.figure(figsize=(12, 6))
plt.scatter(
    df_duration["start_time"],
    df_duration["duration"],
    c=df_duration["color"],
    label="Connections",
    s=10,
)

# Start and End lines
attack_start = plt.axvline(x=20, color="r", linestyle="--", label="Attack Start")
attack_end = plt.axvline(x=120, color="g", linestyle="--", label="Attack End")

plt.xlabel("Connection Start Time (s)")
plt.ylabel("Connection Duration (s)")
plt.title("Connection Duration vs. Connection Start Time")

legend_elements = [
    plt.Line2D(
        [0],
        [0],
        marker="o",
        color="w",
        markerfacecolor="blue",
        markersize=8,
        label="Normal Connections",
    ),
    plt.Line2D(
        [0],
        [0],
        marker="o",
        color="w",
        markerfacecolor="red",
        markersize=8,
        label="Dropped Connections",
    ),
    attack_start,
    attack_end,
]
plt.legend(handles=legend_elements)

plt.grid()
plt.show()
