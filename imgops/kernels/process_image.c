__kernel void process_image(__write_only image2d_t out_tex) {
  int x = get_global_id(0), y = get_global_id(1);
  int2 coords = (int2)(x, y);
  int2 dims = get_image_dim(out_tex);

  if (x >= dims.x || y >= dims.y) return;

  float4 pixel = (float4)((float)x / dims.x, (float)y / dims.y, 0.5f, 1.0f);
  write_imagef(out_tex, coords, pixel);
}