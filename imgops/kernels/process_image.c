__kernel void process_image(__read_only image2d_t in_img, __write_only image2d_t out_tex, const float4 color_mult) {
  const sampler_t sampler = CLK_NORMALIZED_COORDS_FALSE | CLK_ADDRESS_CLAMP_TO_EDGE | CLK_FILTER_NEAREST;
  int2 pos = (int2)(get_global_id(0), get_global_id(1));

  float4 pixel = read_imagef(in_img, sampler, pos) * color_mult;

  write_imagef(out_tex, pos, pixel);
}