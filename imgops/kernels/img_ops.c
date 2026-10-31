__kernel void scale_colors(__read_only image2d_t in_img, __write_only image2d_t out_img, const float4 color_mult) {
  const sampler_t sampler = CLK_NORMALIZED_COORDS_FALSE | CLK_ADDRESS_CLAMP_TO_EDGE | CLK_FILTER_NEAREST;
  int2 pos = (int2)(get_global_id(0), get_global_id(1));

  float4 pixel = read_imagef(in_img, sampler, pos) * color_mult;

  write_imagef(out_img, pos, pixel);
}

__kernel void gamma_correct(__read_write image2d_t img, const int gamma_correct) {
  if (gamma_correct) return;
  int2 pos = (int2)(get_global_id(0), get_global_id(1));

  const float gamma_inv = 0.4545;
  float4 pixel = pow(read_imagef(img, pos), gamma_inv);

  write_imagef(img, pos, pixel);
}