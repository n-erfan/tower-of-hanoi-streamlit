import streamlit as st
import time
import random

# --- Constants ---
PASTEL_COLORS = [
    "#FFB3BA", "#FFDFBA", "#FFFFBA", "#BAFFC9", "#BAE1FF",
    "#E0BAFF", "#BAFFD9", "#FFD6BA", "#D6BAFF", "#BAFFF6"
]
ROD_COLOR = "#222222"
DISK_HEIGHT = 28
ROD_WIDTH = 12

# --- Session State Initialization ---
def init_state():
    if "screen" not in st.session_state:
        st.session_state.screen = "config"
    if "num_towers" not in st.session_state:
        st.session_state.num_towers = 3
    if "num_disks" not in st.session_state:
        st.session_state.num_disks = 3
    if "stack_order" not in st.session_state:
        st.session_state.stack_order = "ascending"
    if "hide_timer" not in st.session_state:
        st.session_state.hide_timer = False
    if "hide_moves" not in st.session_state:
        st.session_state.hide_moves = False
    if "towers" not in st.session_state:
        st.session_state.towers = []
    if "selected_disk" not in st.session_state:
        st.session_state.selected_disk = None
    if "move_count" not in st.session_state:
        st.session_state.move_count = 0
    if "start_time" not in st.session_state:
        st.session_state.start_time = None
    if "timer_running" not in st.session_state:
        st.session_state.timer_running = False
    if "elapsed_time" not in st.session_state:
        st.session_state.elapsed_time = 0.0
    if "game_over" not in st.session_state:
        st.session_state.game_over = False
    if "warning" not in st.session_state:
        st.session_state.warning = ""
    if "last_config" not in st.session_state:
        st.session_state.last_config = {}

def reset_game():
    # Save current config for restart
    st.session_state.last_config = {
        "num_towers": st.session_state.num_towers,
        "num_disks": st.session_state.num_disks,
        "stack_order": st.session_state.stack_order,
        "hide_timer": st.session_state.hide_timer,
        "hide_moves": st.session_state.hide_moves
    }
    # Initialize towers
    towers = [[] for _ in range(st.session_state.num_towers)]
    disks = list(range(1, st.session_state.num_disks + 1))
    if st.session_state.stack_order == "ascending":
        disks = disks[::-1]  # Largest at bottom
    towers[0] = disks.copy()
    st.session_state.towers = towers
    st.session_state.selected_disk = None
    st.session_state.move_count = 0
    st.session_state.start_time = None
    st.session_state.timer_running = False
    st.session_state.elapsed_time = 0.0
    st.session_state.game_over = False
    st.session_state.warning = ""

def restart_game():
    # Use last config to reset
    for k, v in st.session_state.last_config.items():
        st.session_state[k] = v
    reset_game()
    st.session_state.screen = "game"

def new_game():
    st.session_state.screen = "config"

def format_time(elapsed):
    ms = int((elapsed - int(elapsed)) * 1000)
    s = int(elapsed) % 60
    m = int(elapsed) // 60
    return f"{m:02d}:{s:02d}.{ms:03d}"

def is_legal_move(from_rod, to_rod):
    if not st.session_state.towers[from_rod]:
        return False
    disk = st.session_state.towers[from_rod][-1]
    if not st.session_state.towers[to_rod]:
        return True
    top = st.session_state.towers[to_rod][-1]
    if st.session_state.stack_order == "ascending":
        return disk < top
    else:
        return disk > top

def check_win():
    # Win: all disks on any rod except the first, in correct order
    for idx, rod in enumerate(st.session_state.towers):
        if idx == 0:
            continue
        if len(rod) == st.session_state.num_disks:
            # Check order
            if st.session_state.stack_order == "ascending":
                if rod == list(range(st.session_state.num_disks, 0, -1)):
                    return True
            else:
                if rod == list(range(1, st.session_state.num_disks + 1)):
                    return True
    return False

def draw_board():
    # Draw rods and disks using st.pyplot
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle

    num_towers = st.session_state.num_towers
    num_disks = st.session_state.num_disks

    fig, ax = plt.subplots(figsize=(num_towers*2.2, 3.5))
    ax.set_facecolor("white")
    plt.axis("off")

    # Rod positions
    rod_xs = [i*2 for i in range(num_towers)]
    rod_y = 0.5
    rod_h = DISK_HEIGHT * (num_disks+1)/44

    # Draw rods
    for x in rod_xs:
        ax.add_patch(Rectangle((x-ROD_WIDTH/44, rod_y), ROD_WIDTH/22, rod_h, color=ROD_COLOR, zorder=1))

    # Draw disks
    for i, rod in enumerate(st.session_state.towers):
        for j, disk in enumerate(rod):
            disk_width = 0.3 + 1.2 * (disk/num_disks)
            disk_color = PASTEL_COLORS[(disk-1)%len(PASTEL_COLORS)]
            y = rod_y + (j * DISK_HEIGHT/44)
            ax.add_patch(Rectangle((rod_xs[i]-disk_width/2, y), disk_width, DISK_HEIGHT/44, color=disk_color, ec='black', zorder=2, linewidth=1.2))
            # Disk label
            ax.text(rod_xs[i], y + DISK_HEIGHT/88, str(disk), ha='center', va='center', fontsize=10, color="#333", zorder=3)

    ax.set_xlim(-1, rod_xs[-1]+1)
    ax.set_ylim(0, rod_y + rod_h + 0.2)
    st.pyplot(fig, use_container_width=True)

def game_controls():
    col1, col2 = st.columns([1,1])
    with col1:
        if st.button("🔄 Restart"):
            restart_game()
            st.rerun()
    with col2:
        if st.button("🆕 New Game"):
            new_game()
            st.rerun()

def main():
    init_state()
    if st.session_state.screen == "config":
        st.title("Tower of Hanoi")
        with st.form("config_form"):
            num_towers = st.slider("Number of Towers", 3, 5, 3)
            num_disks = st.slider("Number of Disks", 3, 10, 3)
            stack_order = st.radio("Stack Order", ["ascending", "descending"], format_func=lambda x: f"{x.capitalize()} (smallest on top)" if x=="ascending" else "Descending (largest on top)")
            hide_timer = st.checkbox("Hide Timer widget", value=False)
            hide_moves = st.checkbox("Hide Move Counter", value=False)
            submitted = st.form_submit_button("Start")
            if submitted:
                st.session_state.num_towers = num_towers
                st.session_state.num_disks = num_disks
                st.session_state.stack_order = "ascending" if stack_order.startswith("ascending") else "descending"
                st.session_state.hide_timer = hide_timer
                st.session_state.hide_moves = hide_moves
                reset_game()
                st.session_state.screen = "game"
                st.rerun()
        st.info("Configure your Tower of Hanoi game and click Start.")
        return

    # --- Game Screen ---
    # Top bar: Timer and Move Counter (left), Restart/New Game (right)
    top1, top2 = st.columns([3,1])
    with top1:
        if not st.session_state.hide_timer:
            if st.session_state.timer_running:
                st.session_state.elapsed_time = time.perf_counter() - st.session_state.start_time
            st.markdown(f"**⏱️ Timer:** {format_time(st.session_state.elapsed_time)}")
        if not st.session_state.hide_moves:
            st.markdown(f"**🔢 Moves:** {st.session_state.move_count}")
    with top2:
        game_controls()

    # Draw board
    draw_board()

    # --- Disk Move Controls ---
    st.markdown("### Move Disks")
    move_cols = st.columns(st.session_state.num_towers)
    for i in range(st.session_state.num_towers):
        with move_cols[i]:
            # Pick up disk
            if st.session_state.selected_disk is None:
                if st.session_state.towers[i]:
                    if st.button(f"Pick from Rod {i+1}", key=f"pick_{i}"):
                        st.session_state.selected_disk = i
                        st.session_state.warning = ""
                        st.rerun()
            else:
                # Place disk
                if st.button(f"Place on Rod {i+1}", key=f"place_{i}"):
                    from_rod = st.session_state.selected_disk
                    to_rod = i
                    if from_rod == to_rod:
                        st.session_state.warning = "Cannot place on the same rod."
                    elif is_legal_move(from_rod, to_rod):
                        disk = st.session_state.towers[from_rod].pop()
                        st.session_state.towers[to_rod].append(disk)
                        st.session_state.move_count += 1
                        st.session_state.selected_disk = None
                        st.session_state.warning = ""
                        if not st.session_state.timer_running:
                            st.session_state.start_time = time.perf_counter()
                            st.session_state.timer_running = True
                        if check_win():
                            st.session_state.timer_running = False
                            st.session_state.elapsed_time = time.perf_counter() - st.session_state.start_time
                            st.session_state.game_over = True
                        st.rerun()
                    else:
                        st.session_state.warning = "Illegal move! Cannot place disk here."
                        st.session_state.selected_disk = None
                        st.rerun()

    if st.session_state.selected_disk is not None:
        st.info(f"Selected disk from Rod {st.session_state.selected_disk+1}. Now select a rod to place.")

    if st.session_state.warning:
        st.warning(st.session_state.warning)

    if st.session_state.game_over:
        st.success(f"🎉 Congratulations! You solved it in {st.session_state.move_count} moves and {format_time(st.session_state.elapsed_time)}.")
        st.button("Play Again", on_click=restart_game)
        st.button("New Game", on_click=new_game)

if __name__ == "__main__":
    main()
