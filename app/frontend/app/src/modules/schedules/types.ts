export type CommandType =
  | "FOR"
  | "WHILE"
  | "IF"
  | "ELSE"
  | "SET"
  | "END"
  | "WAIT"
  | "TRIGGER";

//functions of either of these types aren't required on front end hence unimplemented
export interface FunctionCode {
  CommandType: CommandType;
  Number: number;
  LinkedCommands?: number[];
  Params?: string[];
}

export interface Schedule {
  ScheduleID: string;
  ScheduleName: string;
  AuthorID: string;
  IsPublic: boolean;
  IsActive: boolean;
  IsDraft: boolean;
  Rating: number; //was just one value, but instead should be a computed value
  Trigger: string[];
  Code: FunctionCode[];
  CustomVars?: Record<string, "NUMBER" | "BOOLEAN">;
}

export interface ListSchedule {
  IsActive: number;
  IsPublic: number;
  IsDraft: number;
  Rating: number;
  ScheduleID: string;
  ScheduleName: string;
}

export interface Trigger {
  id: string;
  data: Record<string, string[]>; //deviceID: data
}

export interface Device {
  id: string;
  name: string;
  isActive: boolean;
  data: Record<string, "NUMBER" | "BOOLEAN">; //string is variable name which is the key, value will be describing the type
}
