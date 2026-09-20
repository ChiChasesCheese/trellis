---
title: Vector tiles introduction | Tilesets | Mapbox Docs
source: https://docs.mapbox.com/data/tilesets/guides/vector-tiles-introduction/
published: '2025-12-02'
site: Mapbox Documentation
clipped: '2026-09-20'
---

# Vector tiles introduction | Tilesets | Mapbox Docs

# Vector tiles introduction

A [**Vector tile**](https://docs.mapbox.com/help/glossary/vector-tiles/) is the vector data equivalent of raster image tiles for web mapping. Vector tiles contain all the strengths of tiling: optimized for caching, scaling, and serving map imagery rapidly, allowing you to make huge maps quickly while offering full design flexibility.

This guide describes how vector tiles work in Mapbox web and mobile maps.

## How web and mobile maps work[](#how-web-and-mobile-maps-work)

Earlier generations of web and mobile maps used image-based tiles known as **raster tiles**. This PNG image tile depicts the corner of lower Manhattan in New York City, showing roads, building footprints, and parks:

To make a map, many such image tiles are stitched together in a grid. Each tile is requested from a URL that specifies the map style, zoom level, and x- and y-coordinates of the tile. The tile above has a zoom level of **14**, and x- and y-coordinates of **4823** and **6160**, respectively. To explore tile addresses, try out our [What the Tile](https://labs.mapbox.com/what-the-tile/) tool.

**Vector tiles** work similarly, but instead of an image of a styled map for a specific area, each tile contains raw geographic data in vector format for that area. They contain geometries and metadata — like road names, place names, house numbers — in a compact, structured format. The image below can help you conceptualize the points, lines, and polygons contained in a vector tile for the same area of lower Manhattan.

*The vector tile itself is not an image, it is compressed vector data.* This means that creating a visually pleasing map requires an additional step of styling and rendering the vector data, which is exactly what Mapbox rendering software does. The rendering happens using various GL technologies, allowing for smooth and efficient map rendering, camera movements, and interactions. Our renderers include [Mapbox GL JS](https://docs.mapbox.com/mapbox-gl-js/guides/) for web projects, the [Maps SDK for iOS](https://docs.mapbox.com/ios/maps/guides/), and the [Maps SDK for Android](https://docs.mapbox.com/android/maps/guides/)

You may hear of "Mapbox Vector Tile" (MVT) format, which is the specific implementation of vector tiles that Mapbox created and open-sourced. MVT is based on the open standard for vector tiles defined in the [Mapbox Vector Tile Specification](https://github.com/mapbox/vector-tile-spec).

Vector tiles may have the extension `.mvt` or `.pbf` (for "protocol buffer format") depending on the context in which they are used.

We also provide APIs that render vector tiles on our servers and return raster images to you, including:

- The [Static Tiles API](https://docs.mapbox.com/api/maps/static-tiles/) returns raster images rendered from vector tiles at specific tile coordinates.
- The [Static Images API](https://docs.mapbox.com/api/maps/static-images/) returns images of arbitrary size and location rendered from vector tiles.

See the [Map design guide](https://docs.mapbox.com/help/getting-started/map-design/) for more information on how map styles work. All Mapbox styles, including the Mapbox Standard Style, are created using some combination of our [Mapbox tilesets](/data/tilesets/reference/).

## Why use vector tiles?[](#benefits-of-vector-tiles)

Vector tiles offer several important advantages over traditional raster tiles:

- 
**Efficiency and scalability** . Vector tiles are lightweight and optimized for large datasets. They scale infinitely, allowing users to zoom in and out without losing map fidelity or requiring new image tiles to be rendered for each zoom level.
- 
**Smooth, dynamic interactions** . Because all map data is loaded as vectors, the map can be re-rendered quickly in the browser or on a device, enabling smooth zooming, panning, tilt, and rotation. Animations and user interactions are much smoother compared to raster tiles.
- 
**Dynamic styling** . Tiles are styled at runtime, allowing for[many map styles](https://www.mapbox.com/gallery) on global data. Using Mapbox GL JS or the Mapbox Maps SDKs for Android and iOS, you can adjust your map's appearance at any time via code, without having to download new tiles.
- 
**Size and speed** . Vector tiles are small, enabling global high-resolution maps, faster map loads, and efficient caching. Mapbox cartographers balance detail and performance in all Mapbox-provided vector tilesets.
- 
**Dynamically querying** . You can access your map data's properties directly from your vector tileset, enabling advanced interactivity and data exploration.

For example, vector tiles store data points and geometries instead of large image files, allowing you to create rich, interactive maps without the overhead of storing and serving heavy raster images.

**When *not* to use vector tiles:**

Rendering vector tiles in the browser or device requires more processing power compared to displaying pre-rendered raster images. On low-powered devices or in environments with limited computational resources, raster tiles may provide a more consistent user experience.

In situations where you do not need users to move around the map, such as static maps or predefined routes, raster tiles or static map images may be more appropriate.

You can still use Mapbox services to style and serve raster tiles in these scenarios, for example you can load a Mapbox-hosted style in leafelet.js using the [Mapbox Raster Tiles API](https://docs.mapbox.com/api/maps/raster-tiles/).

### Side by side comparison of vector tiles and raster tiles[](#side-by-side-comparison-of-vector-tiles-and-raster-tiles)

The map on the left shows vector tiles rendered in the browser using **Mapbox GL JS**, while the map on the right shows raster tiles rendered as images using **leaflet.js**. Notice how the vector map remains crisp and clear at various zoom levels, while the raster map becomes pixelated when zoomed in.

*Vector Tileset*

*Raster Tileset*

Mapbox Streets, our global basemap, is entirely made of vector tiles.

## Open standard[](#open-standard)

Vector tiles are an open standard under a Creative Commons Attribution 3.0 US License. We support vector tiles across our products and there is a [large list of vector tile implementation by other vendors](https://github.com/mapbox/awesome-vector-tiles).

- [Read the Mapbox Vector Tile Spec on GitHub](https://github.com/mapbox/vector-tile-spec) and get in touch with us there with feedback and improvements.
- [See the Vector Tiles Awesome List](https://github.com/mapbox/awesome-vector-tiles) for a curated list of tools and resources related to Mapbox vector tiles.
