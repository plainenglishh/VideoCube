# VideoCube

![Example](./samples/zoo_3d.png)

Converts a video into a series of textures to be applied to the surfaces of a cube, where depth of the cube represents time, using OpenCV.

## Usage

```bash
py . <input> <output_dir> [prefix]
```

This will create six images named in the format `[prefix][face].png`, e.g `left.png`.

