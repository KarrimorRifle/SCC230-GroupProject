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

export interface NewHubDevice {
  DeviceName: string;
  DeviceType: string;
  IpAddress?: string;
}

export interface EditingDevice {
  DeviceID: string;
  DeviceName: string;
  IpAddress: string;
  Key: string;
  Version: number;
  Company: string;
  HubID: string;
  Vars: {
    Name: string;
    Type: string;
    Access: 0 | 1;
  };
}

export interface HubScheduleList {
  ScheduleID: string;
  ScheduleName: string;
  IsActive: boolean;
  Author: string;
  CopyFrom: string | null;
  PermissionLevel: number;
}
