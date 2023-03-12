// @ts-ignore
/* eslint-disable */
import { request } from '@umijs/max';

export enum ApiUrl {
  currentUser='/api/v1/user/current-user',
  login='/api/v1/user/login/account',
  outLogin='/api/v1/user/out-login',
  rule='/api/v1/user/rule',
  captcha='/api/v1/user/login/captcha',
  notices='/api/v1/user/notices'
}

/** 获取当前的用户 GET /api/current-user */
export async function currentUser(options?: { [key: string]: any }) {
  return request<{
    data: API.CurrentUser;
  }>(ApiUrl.currentUser, {
    method: 'GET',
    ...(options || {}),
  });
}

/** 退出登录接口 POST /api/login/out-login */
export async function outLogin(options?: { [key: string]: any }) {
  return request<Record<string, any>>(ApiUrl.outLogin, {
    method: 'POST',
    ...(options || {}),
  });
}

/** 登录接口 POST /api/login/account */
export async function login(body: API.LoginParams, options?: { [key: string]: any }) {
  return request<API.LoginResult>(ApiUrl.login, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    data: body,
    ...(options || {}),
  });
}

/** 此处后端没有提供注释 GET /api/notices */
export async function getNotices(options?: { [key: string]: any }) {
  return request<API.NoticeIconList>(ApiUrl.notices, {
    method: 'GET',
    ...(options || {}),
  });
}

/** 获取规则列表 GET /api/rule */
export async function rule(
  params: {
    // query
    /** 当前的页码 */
    current?: number;
    /** 页面的容量 */
    pageSize?: number;
  },
  options?: { [key: string]: any },
) {
  return request<API.RuleList>(ApiUrl.rule, {
    method: 'GET',
    params: {
      ...params,
    },
    ...(options || {}),
  });
}

/** 新建规则 PUT /api/rule */
export async function updateRule(options?: { [key: string]: any }) {
  return request<API.RuleListItem>(ApiUrl.rule, {
    method: 'PUT',
    ...(options || {}),
  });
}

/** 新建规则 POST /api/rule */
export async function addRule(options?: { [key: string]: any }) {
  return request<API.RuleListItem>(ApiUrl.rule, {
    method: 'POST',
    ...(options || {}),
  });
}

/** 删除规则 DELETE /api/rule */
export async function removeRule(options?: { [key: string]: any }) {
  return request<Record<string, any>>(ApiUrl.rule, {
    method: 'DELETE',
    ...(options || {}),
  });
}


/** 发送验证码 POST /api/login/captcha */
export async function getCaptcha(
  params: {
    // query
    /** 手机号 */
    phone?: string;
  },
  options?: { [key: string]: any },
) {
  return request<API.FakeCaptcha>(ApiUrl.captcha, {
    method: 'GET',
    params: {
      ...params,
    },
    ...(options || {}),
  });
}
