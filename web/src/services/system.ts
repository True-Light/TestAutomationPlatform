// @ts-ignore
/* eslint-disable */
import { request } from '@umijs/max';
import { SelectListResponse, GetUploadUrl } from '@/typings/system'

export enum ApiUrl {
  jobList='/api/v1/system/enum-job-list',
  suiteList='/api/v1/system/enum-suite-list',
  featureList='/api/v1/system/enum-feature-list',
  versionList='/api/v1/system/enum-version-list',
  uploadUrl='/api/v1/system/get-upload-url',
}

/** 获取定时任务名称 GET /api/v1/system/job-list */
export async function getJobList(options?: { [key: string]: any }) {
  return request<SelectListResponse>(ApiUrl.jobList, {
    method: 'GET',
    ...(options || {}),
  });
}

/** 获取集合名称 GET /api/v1/system/suite-list */
export async function getSuiteList(options?: { [key: string]: any }) {
  return request<SelectListResponse>(ApiUrl.suiteList, {
    method: 'GET',
    ...(options || {}),
  });
}

/** 获取功能名称 GET /api/v1/system/feature-list */
export async function getFeatureList(options?: { [key: string]: any }) {
  return request<SelectListResponse>(ApiUrl.featureList, {
    method: 'GET',
    ...(options || {}),
  });
}

/** 获取版本号 GET /api/v1/system/version-list */
export async function getVersionList(options?: { [key: string]: any }) {
  return request<SelectListResponse>(ApiUrl.versionList, {
    method: 'GET',
    ...(options || {}),
  });
}

/** 获取上传地址 GET /api/v1/system/upload-url */
export async function getUploadUrl(options?: { [key: string]: any }) {
  return request<GetUploadUrl>(ApiUrl.uploadUrl, {
    method: 'GET',
    ...(options || {}),
  });
}
