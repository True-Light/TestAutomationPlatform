// allure report 列表页数据
export type AllureReportItem = {
  id?: number;
  uuid?: string;
  job?: string;
  suite?: string;
  feature?: string;
  version?: string;
  url?: string;
  size?: string;
  status?: number;
  createTime?: string;
};

// allure report 查询接口返回值
export type AllureReportListResponse = {
  data?: AllureReportItem[];
  /** 列表的内容总数 */
  total?: number;
  success?: boolean;
};

// allure report 查询请求参数
export type AllureReportParams = {
  /** 当前的页码 */
  current?: number;
  /** 页面的容量 */
  pageSize?: number;
  id?: number;
  uuid?: string;
  job?: string;
  suite?: string;
  feature?: string;
  version?: string;
}

// allure report 上传请求参数
export type UploadAllureReportParams = {
  file?: File;
  remove?: number;
  job?: string;
  suite?: string;
  feature?: string;
  version?: string;
}
