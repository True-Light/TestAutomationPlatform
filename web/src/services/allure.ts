// @ts-ignore
/* eslint-disable */
import { request } from '@umijs/max';
import { AllureReportListResponse, AllureReportParams, UploadAllureReportParams } from '@/typings/allure'

export enum ApiUrl {
  reportList='/api/v1/allure/report-list',
  uploadReport='/api/v1/allure/generate-report-from-zip',
}

/** 获取allure报告列表 POST /api/v1/allure/report-list */
export async function reportList(body: AllureReportParams, options?: { [key: string]: any }) {
  return request<AllureReportListResponse>(ApiUrl.reportList, {
    method: 'POST',
    data: body,
    ...(options || {}),
  });
}

/** 上传allure报告 POST allure/generate-report-from-zip */
export async function uploadReportZip(body: UploadAllureReportParams, options?: { [key: string]: any }) {
  return request<API.ApiResponse>(ApiUrl.uploadReport, {
    method: 'POST',
    data: body,
    ...(options || {}),
  });
}
