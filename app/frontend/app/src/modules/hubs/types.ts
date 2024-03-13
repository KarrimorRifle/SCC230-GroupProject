export interface HubsList {
  HubID: string;
  HubName: string;
  PermissionLevel: number;
  UserCount: number;
}

export interface HubBase {
  HubID: string;
  HubName: string;
  PermissionLevel: number;
}

export interface HubUser {
  AccountID: string;
  Name: string;
  PermissionLevel: number;
}

export interface HubDevice {
  DeviceID: string;
  DeviceName: string;
  Company: string;
}
