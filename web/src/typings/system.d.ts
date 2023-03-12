// 表单选择器选项
export type SelectItem = {
  label: string;
  value: string;
};

// 表单选择器接口返回值
export type SelectListResponse = {
  data: SelectItem[];
  success: boolean;
};


export type GetUploadUrl = {
  success: boolean;
  url: string;
}
