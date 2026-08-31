# Akashganga: A Procedural Portrait of the Milky Way

Akashganga is a procedural digital artwork inspired by the structure and appearance of the Milky Way galaxy.

The artwork is generated entirely through Python code using mathematical functions, procedural noise, probability distributions, and layered rendering techniques. Instead of drawing the galaxy manually, the program defines rules for its spiral structure, stellar populations, gas clouds, dust lanes, galactic core, nebulae, and individual stars.

The result is a different way of looking at Python: not only as a programming language for computation, but as a medium for visual expression.

## The Idea

The Milky Way contains an enormous number of stars, gas clouds, dust lanes, star-forming regions, and a dense galactic centre. Reproducing all of this physically is far beyond the scope of a simple procedural artwork.

Instead, this project creates an artistic approximation using mathematical and stochastic structures.

The galaxy is constructed in layers:

* A dark deep-space background
* A broad galactic disk
* Two logarithmic spiral arms
* Secondary spiral structures for additional density
* Multi-scale procedural cloud textures
* A warm, yellowish galactic core
* Blue-white regions representing hotter stellar and gaseous regions
* Dark dust lanes
* Nebula-like structures
* Dense stellar populations within the galaxy
* Individual background stars
* Bright stars with soft halos
* A small number of diffraction-style stars

The final image emerges from the interaction of these independently generated layers.

## Mathematical Structure

The primary spiral geometry is based on a logarithmic spiral:

```text
r = r₀ exp(kθ)
```

The parameters controlling the spiral determine how tightly the arms wind around the galactic centre.

For every pixel, Cartesian coordinates are transformed into polar coordinates:

```text
r = √(x² + y²)
θ = atan2(y, x)
```

The distance from each point to the spiral arms is then used to create smooth Gaussian-shaped arm structures.

Rather than drawing simple lines, the spiral arms are treated as continuous probability-like fields. This allows them to have width, density, texture, and gradual fading.


## Reproducibility

The artwork uses a fixed NumPy random seed:

```python
np.random.seed(42)
```

This makes the generated artwork reproducible.

Changing the seed produces a different stellar and cloud distribution while retaining the same underlying mathematical structure.

## Requirements

Python 3.9+ is recommended.

Install the required libraries with:

```bash
pip install requirements.txt
```

## Running the Artwork

Clone or download the project and run:

```bash
python milky_way.py
```

The program generates the artwork and saves it as a PNG image.

The output filename is:

```text
Aakashganga.png
```

## Dependencies

The project uses:

* **NumPy** — numerical computation, coordinate transformations, random distributions
* **Matplotlib** — rendering the final artwork
* **SciPy** — Gaussian filtering for procedural cloud and dust textures

No external image assets, fonts, or datasets are required.

## Creative Process

The artwork began as an experiment in generating a Milky Way-like visual using mathematical curves and procedural noise.

The initial challenge was to avoid producing a simple collection of stars or a generic spiral. The galaxy was progressively refined by introducing:

* Logarithmic spiral geometry
* Multiple arm-density layers
* Multi-scale noise
* Dust lanes
* Colour variation
* Stellar populations
* Dense core stars
* Bright stellar points
* Diffused halos
* Diffraction-style stars

The final composition is therefore the result of iterative algorithmic experimentation rather than a manually painted image.

## What Python Contributes

Python is not being used simply to display an already-created image.

The Python program defines the visual rules that create the artwork itself.

Changing mathematical parameters such as spiral tightness, arm width, cloud density, colour intensity, stellar distributions, or the random seed changes the resulting artwork.

This makes the program both the **algorithm and the artistic medium**.

## Artwork

**Title:** Akashganga: A Procedural Portrait of the Milky Way

**Medium:** Generative / Algorithmic Digital Art

**Created with:** Python, NumPy, SciPy, Matplotlib

**Random seed:** 42

**Artist / Coder:** Purva Porwal

