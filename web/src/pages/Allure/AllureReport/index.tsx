import { AllureReportListResponse, AllureReportParams, AllureReportItem, UploadAllureReportParams } from '@/typings/allure'
import { uploadReportZip, reportList } from '@/services/allure';
import { getJobList, getFeatureList, getSuiteList, getVersionList, getUploadUrl } from '@/services/system';
import { PlusOutlined, InboxOutlined } from '@ant-design/icons';
import type { ActionType, ProColumns, ProDescriptionsItemProps } from '@ant-design/pro-components';
import {
  FooterToolbar,
  ModalForm,
  PageContainer,
  ProDescriptions,
  ProFormText,
  ProFormTextArea,
  ProTable,
  DrawerForm,
  ProForm,
  ProFormDateRangePicker,
  ProFormSelect,
  ProFormUploadButton,
  ProFormUploadDragger,
} from '@ant-design/pro-components';
import { FormattedMessage, useIntl } from '@umijs/max';
import { Button, Drawer, Input, message, Upload } from 'antd';
import React, { useRef, useState } from 'react';
import type { UploadProps } from 'antd';

/**
 * @en-US Add node
 * @zh-CN 添加节点
 * @param fields
 */
const handleUpload = async (fields: UploadAllureReportParams) => {
  const hide = message.loading('正在添加');
  try {
    await uploadReportZip(fields);
    hide();
    message.success('上传成功,请等待服务器处理...');
    return true;
  } catch (error) {
    hide();
    message.error('Adding failed, please try again!');
    return false;
  }
};

const ReportList: React.FC = () => {
  /**
   * @en-US Pop-up window of new window
   * @zh-CN 上传窗口的弹窗
   *  */
  const [uploadModalOpen, setUploadModalOpen] = useState<boolean>(false);

  const [showDetail, setShowDetail] = useState<boolean>(false);

  const actionRef = useRef<ActionType>();
  const [currentRow, setCurrentRow] = useState<API.RuleListItem>();
  const [selectedRowsState, setSelectedRows] = useState<API.RuleListItem[]>([]);

  /**
   * @en-US International configuration
   * @zh-CN 国际化配置
   * */
  const intl = useIntl();

  const uploadUrl = async () => {
    let res = await getUploadUrl();
    if (res.success) {
      return res.url
    }
    return ""
  }

  const columns: ProColumns<AllureReportItem>[] = [
    {
      title: (
        <FormattedMessage
          id="pages.allure.reportTable.uuid.title"
          defaultMessage="UUID"
        />
      ),
      hideInSearch: true,
      dataIndex: 'uuid',
      ellipsis: true,
    },
    {
      title: <FormattedMessage id="pages.allure.reportTable.job.title" defaultMessage="Job" />,
      dataIndex: 'job',
      valueType: 'textarea',
      filters: true,
      onFilter: true,
    },
    {
      title: (
        <FormattedMessage
          id="pages.allure.reportTable.suite.title"
          defaultMessage="Suite"
        />
      ),
      dataIndex: 'suite',
      filters: true,
      onFilter: true,
    },
    {
      title: (
        <FormattedMessage
          id="pages.allure.reportTable.feature.title"
          defaultMessage="Feature"
        />
      ),
      dataIndex: 'feature',
      filters: true,
      onFilter: true,
    },
    {
      title: (
        <FormattedMessage
          id="pages.allure.reportTable.version.title"
          defaultMessage="Version"
        />
      ),
      dataIndex: 'version',
      filters: true,
      onFilter: true,
    },
    {
      title: (
        <FormattedMessage
          id="pages.allure.reportTable.url.title"
          defaultMessage="Url"
        />
      ),
      dataIndex: 'id',
      hideInSearch: true,
      render: (_, record) => {
        console.info(window.document.location)
        let serverHost = window.document.location.origin
        let url = serverHost + "/allure-reports/" + record.uuid
        return <a href={url}> {url} </a>
      },
      ellipsis: true,
      // width:'250px',
    },
    {
      title: (
        <FormattedMessage
          id="pages.allure.reportTable.size.title"
          defaultMessage="Size(MB)"
        />
      ),
      hideInSearch: true,
      dataIndex: 'size',
      width:'100px',
    },
    {
      title: <FormattedMessage id="pages.allure.reportTable.status.title" defaultMessage="Status" />,
      dataIndex: 'status',
      hideInSearch: true,
      valueEnum: {
        false: {
          text: (
            <FormattedMessage
              id="pages.allure.reportTable.status.failed"
              defaultMessage="Generated failed"
            />
          ),
          status: 'Error',
        },
        true: {
          text: (
            <FormattedMessage id="pages.allure.reportTable.status.success" defaultMessage="Generated success" />
          ),
          status: 'Success',
        },
      },
      width:'90px',
    },
    {
      title: (
        <FormattedMessage
          id="pages.allure.reportTable.createTime.title"
          defaultMessage="Create"
        />
      ),
      dataIndex: 'createTime',
      hideInSearch: true,
      valueType: 'dateTime',
      width:'150px',
    },
  ];

  return (
    // <PageContainer>
    <div>
      <ProTable<API.RuleListItem, API.PageParams>
        headerTitle={intl.formatMessage({
          id: 'pages.allure.reportTable.title',
          defaultMessage: 'Allure Report',
        })}
        size="small"
        actionRef={actionRef}
        rowKey="id"
        search={{
          labelWidth: 120,
        }}
        toolBarRender={() => [
          <Button
            type="primary"
            key="primary"
            // disabled
            onClick={() => {
              setUploadModalOpen(true);
            }}
          >
            <PlusOutlined /> <FormattedMessage id="pages.allure.reportTable.uploadButton" defaultMessage="Upload" />
          </Button>,
        ]}
        request={reportList}
        columns={columns}
        rowSelection={{
          onChange: (_, selectedRows) => {
            setSelectedRows(selectedRows);
          },
        }}
      />
      <ModalForm
        title={intl.formatMessage({
          id: 'pages.allure.reportTable.UploadModal.title',
          defaultMessage: 'Upload Report',
        })}
        width="450px"
        open={uploadModalOpen}
        onOpenChange={setUploadModalOpen}
        onFinish={async (value) => {
          const success = await handleUpload(value as UploadAllureReportParams);
          if (success) {
            setUploadModalOpen(false);
            actionRef.current?.reload();
          } else {
            message.error("网络不稳定,上传失败了!")
          }
        }}
        modalProps={{
          destroyOnClose: true,
        }}
      >
        <p>请上传allure原始记录压缩文件!</p>
        <ProFormUploadDragger
          extra="仅支持扩展名: .zip!"
          label="allure 结果压缩文件"
          name="file"
          title="上传文件"
          rules={[
            {
              required: true,
              message: (
                <FormattedMessage
                  id="pages.allure.uploadReportForm.file.rule"
                  defaultMessage="Zip file is required!"
                />
              ),
            },
          ]}
          fieldProps={{
            action: uploadUrl,
            accept: 'application/zip, application/x-zip-compress',
            maxCount: 1,
        }}
        />
        {/*<ProFormSelect*/}
        {/*  name="remove"*/}
        {/*  label={intl.formatMessage({*/}
        {/*    id: 'pages.allure.uploadReportForm.remove.title',*/}
        {/*    defaultMessage: 'Remove zip after extracted',*/}
        {/*  })}*/}
        {/*  request={async () => [*/}
        {/*    {label: 'Yes', value: 1},*/}
        {/*    {label: 'No', value: 0},*/}
        {/*  ]}*/}
        {/*  initialValue={1}*/}
        {/*  placeholder={intl.formatMessage({*/}
        {/*    id: 'pages.allure.uploadReportForm.remove.placeholder',*/}
        {/*    defaultMessage: 'Please select yes or no',*/}
        {/*  })}*/}
        {/*  rules={[*/}
        {/*    {*/}
        {/*      required: true,*/}
        {/*      message: (*/}
        {/*        <FormattedMessage*/}
        {/*          id="pages.allure.uploadReportForm.remove.rule"*/}
        {/*          defaultMessage="remove yes or no is required!"*/}
        {/*        />*/}
        {/*      ),*/}
        {/*    },*/}
        {/*  ]}*/}
        {/*/>*/}
        <ProFormSelect
          name="job"
          label={intl.formatMessage({
            id: 'pages.allure.uploadReportForm.job.title',
            defaultMessage: 'Job Name',
          })}
          request={async () => {
            let res = await getJobList();
            if (res.success) {
              return res.data;
            } else {
              message.error('获取工作流列表失败!');
              return [];
            }
          }}
          // tooltip={intl.formatMessage({
          //   id: 'pages.allure.uploadReportForm.job.tooltip',
          //   defaultMessage: 'Max 64 code!',
          // })}
          placeholder={intl.formatMessage({
            id: 'pages.allure.uploadReportForm.job.placeholder',
            defaultMessage: 'Please select a job',
          })}
          rules={[
            {
              required: true,
              message: (
                <FormattedMessage
                  id="pages.allure.uploadReportForm.job.rule"
                  defaultMessage="Job Name is required!"
                />
              ),
            },
          ]}
        />
        <ProFormSelect
          name="suite"
          label={intl.formatMessage({
            id: 'pages.allure.uploadReportForm.suite.title',
            defaultMessage: 'Suite Name',
          })}
          request={async () => {
            let res = await getSuiteList();
            if (res.success) {
              return res.data;
            } else {
              message.error('获取集合列表失败!');
              return [];
            }
          }}
          placeholder={intl.formatMessage({
            id: 'pages.allure.uploadReportForm.suite.placeholder',
            defaultMessage: 'Please select a suite',
          })}
          rules={[
            {
              required: true,
              message: (
                <FormattedMessage
                  id="pages.allure.uploadReportForm.suite.rule"
                  defaultMessage="Suite Name is required!"
                />
              ),
            },
          ]}
        />
        <ProFormSelect
          name="feature"
          label={intl.formatMessage({
            id: 'pages.allure.uploadReportForm.feature.title',
            defaultMessage: 'Feature Name',
          })}
          request={async () => {
            let res = await getFeatureList();
            if (res.success) {
            return res.data;
          } else {
            message.error('获取功能列表失败!');
            return [];
          }
          }}
          placeholder={intl.formatMessage({
            id: 'pages.allure.uploadReportForm.feature.placeholder',
            defaultMessage: 'Please select a feature',
          })}
          rules={[
            {
              required: true,
              message: (
                <FormattedMessage
                  id="pages.allure.uploadReportForm.feature.rule"
                  defaultMessage="Feature Name is required!"
                />
              ),
            },
          ]}
        />
        <ProFormSelect
          name="version"
          label={intl.formatMessage({
            id: 'pages.allure.uploadReportForm.version.title',
            defaultMessage: 'Version',
          })}
          request={async () => {
            let res = await getVersionList();
            if (res.success) {
              return res.data;
            } else {
              message.error('获取版本列表失败!');
              return [];
            }
          }}
          placeholder={intl.formatMessage({
            id: 'pages.allure.uploadReportForm.version.placeholder',
            defaultMessage: 'Please select a version',
          })}
          rules={[
            {
              required: true,
              message: (
                <FormattedMessage
                  id="pages.allure.uploadReportForm.version.rule"
                  defaultMessage="Version is required!"
                />
              ),
            },
          ]}
        />
      </ModalForm>
    </div>
    // </PageContainer>
  );
};

export default ReportList;
