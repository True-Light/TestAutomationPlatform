import { JSEncrypt } from 'jsencrypt';

export function encryptWithRSA(str: string): string {
  const publicKey = "-----BEGIN PUBLIC KEY-----\n" +
    "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDGZRa4gKXTviTiLGhbaBwrt4VU\n" +
    "5DkIvsXKG7IrzmW3BGZwODtJsLtsgZ65EPMjfHiKBZzBS+o3YQpauw71kvibZDSF\n" +
    "EJYlyyhtp1Th4I7sTFUaxlbfUXHOqfWhMILaKJKW70DR5wY8q17Mnn6TLQRXmaNH\n" +
    "Y/WVuU9cHdo1mOdWdwIDAQAB\n" +
    "-----END PUBLIC KEY-----";
  const encrypt = new JSEncrypt();
  encrypt.setPublicKey(publicKey);
  const encrypted = encrypt.encrypt(str);
  if (encrypted) {
    return encrypted;
  } else {
    console.error('加密信息失败!')
    return "";
  }
}
