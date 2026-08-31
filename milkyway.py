import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter

# ============================================================
# Aakashganga (Milkyway)
# ============================================================

np.random.seed(42)

WIDTH = 1400
HEIGHT = 1400

x = np.linspace(-1, 1, WIDTH)
y = np.linspace(-1, 1, HEIGHT)

X, Y = np.meshgrid(x, y)

R = np.sqrt(X**2 + Y**2)
THETA = np.arctan2(Y, X)

R_SAFE = np.maximum(R, 0.025)


# ============================================================
# 1. DARK SPACE
# ============================================================

image = np.zeros(
    (HEIGHT, WIDTH, 3)
)

image[:, :, 0] = 0.001
image[:, :, 1] = 0.002
image[:, :, 2] = 0.012


# ============================================================
# 2. GALACTIC DISK
# ============================================================

disk = np.exp(
    -(R / 0.78) ** 2
)

disk *= np.exp(
    -(R / 0.88) ** 9
)


# ============================================================
# 3. LOGARITHMIC SPIRAL GEOMETRY
# ============================================================

# r = r0 * exp(k theta)
#
# Smaller k -> tighter winding
#
# We use a relatively small k so the arms wrap around
# the centre several times.

r0 = 0.055

k = 0.60

spiral_theta = (
    np.log(
        R_SAFE / r0
    )
    / k
)


# ============================================================
# 4. TWO PRIMARY ARMS
# ============================================================

delta1 = np.angle(
    np.exp(
        1j *
        (
            THETA
            -
            spiral_theta
        )
    )
)

delta2 = np.angle(
    np.exp(
        1j *
        (
            THETA
            -
            spiral_theta
            -
            np.pi
        )
    )
)


# Convert angular distance to physical distance
distance1 = (
    R_SAFE
    * delta1
)

distance2 = (
    R_SAFE
    * delta2
)


# Broad primary arms
ARM_WIDTH = 0.215

arm1 = np.exp(
    -0.5 *
    (
        distance1
        /
        ARM_WIDTH
    ) ** 2
)

arm2 = np.exp(
    -0.5 *
    (
        distance2
        /
        ARM_WIDTH
    ) ** 2
)


primary_arms = (
    arm1
    +
    arm2
)


# ============================================================
# 5. ARM FADE
# ============================================================

inner_fade = (
    1
    -
    np.exp(
        -(R / 0.12) ** 4
    )
)

outer_fade = np.exp(
    -(R / 0.95) ** 5
)

primary_arms *= (
    inner_fade
    *
    outer_fade
)


# ============================================================
# 6. SECONDARY SPIRAL STRUCTURE
# ============================================================

# Instead of adding two more full arms,
# create weaker offset structures.
#
# This makes the galaxy look dense and natural.

secondary_k = 0.205

secondary_theta = (
    np.log(
        R_SAFE / 0.065
    )
    /
    secondary_k
)


delta3 = np.angle(
    np.exp(
        1j *
        (
            THETA
            -
            secondary_theta
            -
            0.45
        )
    )
)

delta4 = np.angle(
    np.exp(
        1j *
        (
            THETA
            -
            secondary_theta
            -
            np.pi
            -
            0.45
        )
    )
)


secondary_width = 0.18

secondary1 = np.exp(
    -0.5 *
    (
        R_SAFE * delta3
        /
        secondary_width
    ) ** 2
)

secondary2 = np.exp(
    -0.5 *
    (
        R_SAFE * delta4
        /
        secondary_width
    ) ** 2
)


secondary = (
    secondary1
    +
    secondary2
)


secondary *= (
    inner_fade
    *
    outer_fade
)


# Secondary arms should be much weaker
secondary *= 0.52


# ============================================================
# 7. COMBINE SPIRAL STRUCTURE
# ============================================================

spiral = (
    primary_arms
    +
    secondary
)


# ============================================================
# 8. MULTI-SCALE CLOUDS
# ============================================================

large_noise = gaussian_filter(
    np.random.random(
        (HEIGHT, WIDTH)
    ),
    sigma=38
)

large_noise -= large_noise.min()
large_noise /= large_noise.max()


medium_noise = gaussian_filter(
    np.random.random(
        (HEIGHT, WIDTH)
    ),
    sigma=14
)

medium_noise -= medium_noise.min()
medium_noise /= medium_noise.max()


small_noise = gaussian_filter(
    np.random.random(
        (HEIGHT, WIDTH)
    ),
    sigma=5
)

small_noise -= small_noise.min()
small_noise /= small_noise.max()


cloud_texture = (
    0.35
    +
    0.65 * large_noise
    +
    0.35 * medium_noise
    +
    0.12 * small_noise
)


# ============================================================
# 9. DENSE SPIRAL CLOUD
# ============================================================

spiral_cloud = (
    spiral
    *
    cloud_texture
)


# ============================================================
# 10. BROAD MILKY WAY GLOW
# ============================================================

broad_glow = (
    disk
    *
    np.exp(
        -(Y / 0.34) ** 2
    )
)


image[:, :, 0] += (
    0.045
    * broad_glow
)

image[:, :, 1] += (
    0.065
    * broad_glow
)

image[:, :, 2] += (
    0.14
    * broad_glow
)


# ============================================================
# 11. BRIGHT SPIRAL ARMS
# ============================================================

image[:, :, 0] += (
    0.19
    * spiral_cloud
)

image[:, :, 1] += (
    0.22
    * spiral_cloud
)

image[:, :, 2] += (
    0.34
    * spiral_cloud
)


# ============================================================
# 12. GALACTIC CORE
# ============================================================

core = np.exp(
    -(
        (X / 0.25) ** 2
        +
        (Y / 0.18) ** 2
    )
)


# Golden / yellow component
image[:, :, 0] += (
    0.48
    * core
)

image[:, :, 1] += (
    0.34
    * core
)

image[:, :, 2] += (
    0.13
    * core
)


# ============================================================
# 13. WHITE-BLUE CENTRAL LIGHT
# ============================================================

hot_core = np.exp(
    -(
        (X / 0.115) ** 2
        +
        (Y / 0.085) ** 2
    )
)


image[:, :, 0] += (
    0.30
    * hot_core
)

image[:, :, 1] += (
    0.34
    * hot_core
)

image[:, :, 2] += (
    0.42
    * hot_core
)


# ============================================================
# 14. CLOUDY CORE
# ============================================================

core_texture = (
    core
    *
    (
        0.35
        +
        1.3 * large_noise
        +
        0.45 * medium_noise
    )
)


image[:, :, 0] += (
    0.20
    * core_texture
)

image[:, :, 1] += (
    0.15
    * core_texture
)

image[:, :, 2] += (
    0.08
    * core_texture
)


# ============================================================
# 15. STAR-FORMING CLUMPS
# ============================================================

# Small bright patches distributed through spiral arms

clump_noise = gaussian_filter(
    np.random.random(
        (HEIGHT, WIDTH)
    ),
    sigma=7
)

clump_noise -= clump_noise.min()
clump_noise /= clump_noise.max()


clumps = (
    spiral
    *
    clump_noise
)


# Keep only strongest regions
clumps = np.maximum(
    clumps - 0.58,
    0
)

clumps = clumps ** 2


image[:, :, 0] += (
    0.07
    * clumps
)

image[:, :, 1] += (
    0.09
    * clumps
)

image[:, :, 2] += (
    0.13
    * clumps
)


# ============================================================
# 16. DARK DUST LANES
# ============================================================

dust_noise = gaussian_filter(
    np.random.random(
        (HEIGHT, WIDTH)
    ),
    sigma=10
)

dust_noise -= dust_noise.min()
dust_noise /= dust_noise.max()


dust = (
    primary_arms
    *
    dust_noise
)


dust = np.maximum(
    dust - 0.42,
    0
)

dust = dust ** 1.6


# Brown/black dust
image[:, :, 0] -= (
    0.22
    * dust
)

image[:, :, 1] -= (
    0.17
    * dust
)

image[:, :, 2] -= (
    0.10
    * dust
)


# ============================================================
# 17. BLUE NEBULAE
# ============================================================

nebula_noise = gaussian_filter(
    np.random.random(
        (HEIGHT, WIDTH)
    ),
    sigma=20
)

nebula_noise -= nebula_noise.min()
nebula_noise /= nebula_noise.max()


nebula = (
    primary_arms
    *
    nebula_noise
)

nebula = np.maximum(
    nebula - 0.58,
    0
)


image[:, :, 0] += (
    0.025
    * nebula
)

image[:, :, 1] += (
    0.045
    * nebula
)

image[:, :, 2] += (
    0.16
    * nebula
)

# ============================================================
# 17B. COLOURED NEBULAR GAS
# ============================================================

# ------------------------------------------------------------
# H-alpha regions — warm red/pink emission
# Young stars ionize surrounding hydrogen.
# ------------------------------------------------------------

h_alpha_noise = gaussian_filter(
    np.random.random((HEIGHT, WIDTH)),
    sigma=9
)

h_alpha_noise -= h_alpha_noise.min()
h_alpha_noise /= h_alpha_noise.max()

h_alpha = (
    primary_arms
    * h_alpha_noise
)

h_alpha = np.maximum(
    h_alpha - 0.52,
    0
)

h_alpha = h_alpha ** 1.8

image[:, :, 0] += 0.16 * h_alpha
image[:, :, 1] += 0.025 * h_alpha
image[:, :, 2] += 0.045 * h_alpha


# ------------------------------------------------------------
# OIII / ionized oxygen — cyan/blue regions
# ------------------------------------------------------------

oiii_noise = gaussian_filter(
    np.random.random((HEIGHT, WIDTH)),
    sigma=12
)

oiii_noise -= oiii_noise.min()
oiii_noise /= oiii_noise.max()

oiii = (
    primary_arms
    * oiii_noise
)

oiii = np.maximum(
    oiii - 0.55,
    0
)

oiii = oiii ** 1.7

image[:, :, 0] += 0.015 * oiii
image[:, :, 1] += 0.075 * oiii
image[:, :, 2] += 0.19 * oiii


# ------------------------------------------------------------
# BLUE REFLECTION NEBULAE
# ------------------------------------------------------------

blue_cloud = gaussian_filter(
    np.random.random((HEIGHT, WIDTH)),
    sigma=25
)

blue_cloud -= blue_cloud.min()
blue_cloud /= blue_cloud.max()

blue_nebula = (
    disk
    * blue_cloud
    * np.exp(-(Y / 0.42) ** 2)
)

blue_nebula = np.maximum(
    blue_nebula - 0.58,
    0
)

image[:, :, 0] += 0.015 * blue_nebula
image[:, :, 1] += 0.035 * blue_nebula
image[:, :, 2] += 0.11 * blue_nebula


# ------------------------------------------------------------
# GOLDEN DUST / WARM GAS
# ------------------------------------------------------------

warm_cloud = gaussian_filter(
    np.random.random((HEIGHT, WIDTH)),
    sigma=18
)

warm_cloud -= warm_cloud.min()
warm_cloud /= warm_cloud.max()

warm_gas = (
    broad_glow
    * warm_cloud
)

warm_gas = np.maximum(
    warm_gas - 0.42,
    0
)

image[:, :, 0] += 0.075 * warm_gas
image[:, :, 1] += 0.035 * warm_gas
image[:, :, 2] += 0.008 * warm_gas


# ============================================================
# 18. FINAL GALAXY
# ============================================================

image = np.clip(
    image,
    0,
    1
)


# ============================================================
# 19. RENDER
# ============================================================

fig, ax = plt.subplots(
    figsize=(12, 12),
    dpi=120
)

ax.imshow(
    image,
    origin="lower",
    extent=[
        -1,
        1,
        -1,
        1
    ]
)


# ============================================================
# 20. STAR FIELD
# ============================================================

# We deliberately use several populations of stars.
#
# 1. Extremely faint background stars
# 2. Dense Milky Way stars
# 3. Young blue stars along spiral arms
# 4. Warm/yellow stars
# 5. Rare bright stars
# 6. Diffraction stars
#
# This avoids the "white dot wallpaper" appearance.


# ============================================================
# 20A. DISTANT BACKGROUND STARS
# ============================================================

N_BACKGROUND = 32000

background_x = np.random.uniform(
    -1,
    1,
    N_BACKGROUND
)

background_y = np.random.uniform(
    -1,
    1,
    N_BACKGROUND
)

background_sizes = np.random.choice(
    [
        0.025,
        0.05,
        0.08,
        0.12,
        0.18,
        0.28
    ],
    N_BACKGROUND,
    p=[
        0.30,
        0.27,
        0.20,
        0.13,
        0.075,
        0.025
    ]
)

background_alpha = np.random.exponential(
    0.055,
    N_BACKGROUND
)

background_alpha = np.clip(
    background_alpha,
    0.008,
    0.20
)

background_colors = np.random.choice(
    [
        "#ffffff",
        "#eaf4ff",
        "#fff4d6",
        "#d8eaff"
    ],
    N_BACKGROUND,
    p=[
        0.60,
        0.18,
        0.12,
        0.10
    ]
)

ax.scatter(
    background_x,
    background_y,
    s=background_sizes,
    c=background_colors,
    alpha=background_alpha,
    linewidths=0
)


# ============================================================
# 20B. DENSE MILKY WAY STAR POPULATION
# ============================================================

N_GALAXY = 60000

galaxy_r = (
    np.random.power(
        1.9,
        N_GALAXY
    )
    * 0.97
)

galaxy_theta = np.random.uniform(
    0,
    2 * np.pi,
    N_GALAXY
)


galaxy_x = (
    galaxy_r
    * np.cos(galaxy_theta)
)

galaxy_y = (
    galaxy_r
    * np.sin(galaxy_theta)
)


# ------------------------------------------------------------
# Distance from spiral arms
# ------------------------------------------------------------

star_r_safe = np.maximum(
    galaxy_r,
    0.025
)

star_spiral_theta = (
    np.log(
        star_r_safe / r0
    )
    / k
)


star_delta1 = np.angle(
    np.exp(
        1j *
        (
            galaxy_theta
            -
            star_spiral_theta
        )
    )
)

star_delta2 = np.angle(
    np.exp(
        1j *
        (
            galaxy_theta
            -
            star_spiral_theta
            -
            np.pi
        )
    )
)

star_arm_distance = np.minimum(
    np.abs(star_delta1),
    np.abs(star_delta2)
)


# ------------------------------------------------------------
# Arm concentration
# ------------------------------------------------------------

arm_probability = np.exp(
    -(
        star_r_safe
        * star_arm_distance
        / 0.17
    ) ** 2
)


# ------------------------------------------------------------
# Star brightness
# ------------------------------------------------------------

galaxy_alpha = (
    0.025
    +
    0.28 * arm_probability
)

galaxy_alpha *= np.random.lognormal(
    mean=-0.35,
    sigma=0.65,
    size=N_GALAXY
)

galaxy_alpha = np.clip(
    galaxy_alpha,
    0.008,
    0.48
)


# ------------------------------------------------------------
# Mostly microscopic stars
# ------------------------------------------------------------

galaxy_sizes = np.random.choice(
    [
        0.025,
        0.05,
        0.08,
        0.12,
        0.18,
        0.28,
        0.42,
        0.65
    ],
    N_GALAXY,
    p=[
        0.20,
        0.22,
        0.20,
        0.15,
        0.10,
        0.07,
        0.045,
        0.015
    ]
)


galaxy_colors = np.random.choice(
    [
        "#ffffff",
        "#e8f3ff",
        "#c9e4ff",
        "#fff4d2",
        "#ffdca8"
    ],
    N_GALAXY,
    p=[
        0.46,
        0.20,
        0.12,
        0.14,
        0.08
    ]
)


ax.scatter(
    galaxy_x,
    galaxy_y,
    s=galaxy_sizes,
    c=galaxy_colors,
    alpha=galaxy_alpha,
    linewidths=0
)


# ============================================================
# 21. YOUNG BLUE STARS IN SPIRAL ARMS
# ============================================================

N_BLUE = 4500

blue_r = np.random.uniform(
    0.10,
    0.91,
    N_BLUE
)

blue_r_safe = np.maximum(
    blue_r,
    0.025
)

blue_spiral_theta = (
    np.log(
        blue_r_safe / r0
    )
    / k
)


blue_arm = np.random.choice(
    [0, 1],
    N_BLUE
)


blue_theta = (
    blue_spiral_theta
    +
    blue_arm * np.pi
    +
    np.random.normal(
        0,
        0.12,
        N_BLUE
    )
)


blue_x = (
    blue_r
    * np.cos(blue_theta)
)

blue_y = (
    blue_r
    * np.sin(blue_theta)
)


blue_sizes = np.random.lognormal(
    mean=-0.2,
    sigma=0.65,
    size=N_BLUE
)

blue_sizes = np.clip(
    blue_sizes,
    0.15,
    2.5
)


blue_alpha = np.random.uniform(
    0.12,
    0.75,
    N_BLUE
)


ax.scatter(
    blue_x,
    blue_y,
    s=blue_sizes,
    c="#b9ddff",
    alpha=blue_alpha,
    linewidths=0
)


# ============================================================
# 22. WARM / GOLDEN STARS
# ============================================================

N_WARM = 3500

warm_r = np.random.power(
    1.45,
    N_WARM
) * 0.72

warm_theta = np.random.uniform(
    0,
    2 * np.pi,
    N_WARM
)

warm_x = (
    warm_r
    * np.cos(warm_theta)
)

warm_y = (
    warm_r
    * np.sin(warm_theta)
)

warm_sizes = np.random.lognormal(
    mean=-0.35,
    sigma=0.6,
    size=N_WARM
)

warm_sizes = np.clip(
    warm_sizes,
    0.12,
    1.8
)

ax.scatter(
    warm_x,
    warm_y,
    s=warm_sizes,
    c="#ffd995",
    alpha=np.random.uniform(
        0.10,
        0.55,
        N_WARM
    ),
    linewidths=0
)


# ============================================================
# 23. REALISTIC LARGE STARS
# ============================================================

# Large stars are built from:
#
#   1. diffuse halo
#   2. elongated optical glow
#   3. soft diffraction rays
#   4. tiny bright stellar core
#
# This prevents them from looking like large white dots.

N_LARGE = 180

large_x = np.random.uniform(
    -1,
    1,
    N_LARGE
)

large_y = np.random.uniform(
    -1,
    1,
    N_LARGE
)

large_sizes = np.random.lognormal(
    mean=0.65,
    sigma=0.50,
    size=N_LARGE
)

large_sizes = np.clip(
    large_sizes,
    2.5,
    9
)

large_colors = np.random.choice(
    [
        "#ffffff",
        "#eaf5ff",
        "#d8edff",
        "#fff3d2",
        "#ffe4b8"
    ],
    N_LARGE,
    p=[
        0.38,
        0.22,
        0.14,
        0.17,
        0.09
    ]
)


for sx, sy, size, color in zip(
    large_x,
    large_y,
    large_sizes,
    large_colors
):

    # --------------------------------------------------------
    # 1. Very soft stellar halo
    # --------------------------------------------------------

    ax.scatter(
        sx,
        sy,
        s=size * 180,
        c=color,
        alpha=0.006,
        linewidths=0
    )

    ax.scatter(
        sx,
        sy,
        s=size * 70,
        c=color,
        alpha=0.015,
        linewidths=0
    )


    # --------------------------------------------------------
    # 2. Subtle optical glow
    # --------------------------------------------------------

    ax.scatter(
        sx,
        sy,
        s=size * 20,
        c=color,
        alpha=0.035,
        linewidths=0
    )


    # --------------------------------------------------------
    # 3. Soft diffraction
    # --------------------------------------------------------

    # Only some large stars receive visible diffraction.
    # This is critical for realism.

    if np.random.random() < 0.32:

        rotation = np.random.uniform(
            0,
            np.pi
        )

        # Two dominant optical axes
        # create a natural photographic starburst.

        for axis in range(2):

            angle = (
                rotation
                +
                axis * np.pi / 2
            )

            length = np.random.uniform(
                0.018,
                0.045
            )

            # Slight asymmetry
            left = np.random.uniform(
                0.65,
                0.95
            )

            right = np.random.uniform(
                0.75,
                1.15
            )

            x1 = (
                sx
                -
                np.cos(angle)
                * length
                * left
            )

            y1 = (
                sy
                -
                np.sin(angle)
                * length
                * left
            )

            x2 = (
                sx
                +
                np.cos(angle)
                * length
                * right
            )

            y2 = (
                sy
                +
                np.sin(angle)
                * length
                * right
            )


            # Broad atmospheric ray

            ax.plot(
                [x1, x2],
                [y1, y2],
                color=color,
                alpha=0.025,
                linewidth=2.0,
                solid_capstyle="round"
            )

            # Thin inner ray

            ax.plot(
                [
                    sx - (sx - x1) * 0.65,
                    sx + (x2 - sx) * 0.65
                ],
                [
                    sy - (sy - y1) * 0.65,
                    sy + (y2 - sy) * 0.65
                ],
                color="#ffffff",
                alpha=0.055,
                linewidth=0.45,
                solid_capstyle="round"
            )


    # --------------------------------------------------------
    # 4. Bright stellar core
    # --------------------------------------------------------

    # Tiny core rather than a large white circle.

    ax.scatter(
        sx,
        sy,
        s=size * 1.8,
        c=color,
        alpha=0.35,
        linewidths=0
    )

    ax.scatter(
        sx,
        sy,
        s=max(0.5, size * 0.45),
        c="#ffffff",
        alpha=0.98,
        linewidths=0
    )


# ============================================================
# 24. SPECIAL SIX-RAY PHOTOGRAPHIC STARS
# ============================================================

# These are the stars that should visibly resemble
# the classic diffraction stars seen in astrophotography.
#
# Very few are used.

N_SPECIAL = 18

special_x = np.random.uniform(
    -0.92,
    0.92,
    N_SPECIAL
)

special_y = np.random.uniform(
    -0.92,
    0.92,
    N_SPECIAL
)


for sx, sy in zip(
    special_x,
    special_y
):

    size = np.random.uniform(
        6,
        11
    )

    strength = np.random.uniform(
        0.65,
        1.0
    )

    color = np.random.choice(
        [
            "#ffffff",
            "#e7f4ff",
            "#fff0c9"
        ]
    )


    # --------------------------------------------------------
    # Large diffuse halo
    # --------------------------------------------------------

    ax.scatter(
        sx,
        sy,
        s=size * 240,
        c=color,
        alpha=0.006 * strength,
        linewidths=0
    )

    ax.scatter(
        sx,
        sy,
        s=size * 80,
        c=color,
        alpha=0.018 * strength,
        linewidths=0
    )


    # --------------------------------------------------------
    # Six optical rays
    # --------------------------------------------------------

    rotation = np.random.uniform(
        0,
        np.pi / 6
    )

    for ray in range(3):

        angle = (
            rotation
            +
            ray * np.pi / 3
        )

        # Each side gets slightly different length

        length1 = np.random.uniform(
            0.018,
            0.040
        )

        length2 = np.random.uniform(
            0.022,
            0.052
        )


        # ----------------------------------------------------
        # First side
        # ----------------------------------------------------

        x1 = (
            sx
            +
            np.cos(angle)
            * length1
        )

        y1 = (
            sy
            +
            np.sin(angle)
            * length1
        )


        # ----------------------------------------------------
        # Opposite side
        # ----------------------------------------------------

        x2 = (
            sx
            -
            np.cos(angle)
            * length2
        )

        y2 = (
            sy
            -
            np.sin(angle)
            * length2
        )


        # Broad diffuse ray

        ax.plot(
            [x1, x2],
            [y1, y2],
            color=color,
            alpha=0.025 * strength,
            linewidth=2.2,
            solid_capstyle="round"
        )

        # Thin central ray

        ax.plot(
            [
                sx + (x1 - sx) * 0.15,
                sx + (x2 - sx) * 0.65
            ],
            [
                sy + (y1 - sy) * 0.15,
                sy + (y2 - sy) * 0.65
            ],
            color="#ffffff",
            alpha=0.07 * strength,
            linewidth=0.5,
            solid_capstyle="round"
        )


    # --------------------------------------------------------
    # Tiny hot core
    # --------------------------------------------------------

    ax.scatter(
        sx,
        sy,
        s=size * 2.5,
        c=color,
        alpha=0.18,
        linewidths=0
    )

    ax.scatter(
        sx,
        sy,
        s=size * 0.45,
        c="#ffffff",
        alpha=1.0,
        linewidths=0
    )


# ============================================================
# 25. A FEW VERY BRIGHT NATURAL STARS
# ============================================================

# These don't have obvious spikes.
# They are simply intense stars with strong atmospheric glow.

hero_stars = [
    (-0.80, 0.68, 8.5),
    (0.73, 0.58, 7.5),
    (-0.67, -0.72, 7.0),
    (0.82, -0.32, 6.5),
    (0.55, -0.76, 6.0),
    (-0.88, -0.18, 5.5),
]


for sx, sy, size in hero_stars:

    # Huge faint halo
    ax.scatter(
        sx,
        sy,
        s=size * 220,
        c="#eaf5ff",
        alpha=0.005,
        linewidths=0
    )

    # Medium halo
    ax.scatter(
        sx,
        sy,
        s=size * 70,
        c="#ffffff",
        alpha=0.015,
        linewidths=0
    )

    # Small luminous region
    ax.scatter(
        sx,
        sy,
        s=size * 8,
        c="#ffffff",
        alpha=0.10,
        linewidths=0
    )

    # Actual stellar point
    ax.scatter(
        sx,
        sy,
        s=size * 0.55,
        c="#ffffff",
        alpha=1.0,
        linewidths=0
    )


# ============================================================
# 26. MICRO STAR DUST
# ============================================================

N_MICRO = 70000

micro_x = np.random.uniform(
    -1,
    1,
    N_MICRO
)

micro_y = np.random.uniform(
    -1,
    1,
    N_MICRO
)

micro_sizes = np.random.uniform(
    0.008,
    0.065,
    N_MICRO
)

micro_alpha = np.random.uniform(
    0.006,
    0.050,
    N_MICRO
)

micro_colors = np.random.choice(
    [
        "#ffffff",
        "#e9f4ff",
        "#fff2cf"
    ],
    N_MICRO,
    p=[
        0.62,
        0.25,
        0.13
    ]
)

ax.scatter(
    micro_x,
    micro_y,
    s=micro_sizes,
    c=micro_colors,
    alpha=micro_alpha,
    linewidths=0
)

# ============================================================
# 27. FINAL MICRO STAR FIELD
# ============================================================

# Extremely tiny stars create the photographic grain
# throughout the entire sky.

N_MICRO = 60000

micro_x = np.random.uniform(
    -1,
    1,
    N_MICRO
)

micro_y = np.random.uniform(
    -1,
    1,
    N_MICRO
)

micro_sizes = np.random.uniform(
    0.01,
    0.07,
    N_MICRO
)

micro_alpha = np.random.uniform(
    0.008,
    0.055,
    N_MICRO
)

micro_colors = np.random.choice(
    [
        "#ffffff",
        "#eaf4ff",
        "#fff3d0"
    ],
    N_MICRO,
    p=[
        0.65,
        0.22,
        0.13
    ]
)

ax.scatter(
    micro_x,
    micro_y,
    s=micro_sizes,
    c=micro_colors,
    alpha=micro_alpha,
    linewidths=0
)


# ============================================================
# 28. FINAL RENDER
# ============================================================

ax.set_xlim(
    -1,
    1
)

ax.set_ylim(
    -1,
    1
)

ax.set_aspect(
    "equal"
)

ax.axis("off")

plt.tight_layout(
    pad=0
)

plt.savefig(
    "aakashganga_final_starry.png",
    dpi=220,
    bbox_inches="tight",
    pad_inches=0,
    facecolor="#01020a"
)

plt.show()