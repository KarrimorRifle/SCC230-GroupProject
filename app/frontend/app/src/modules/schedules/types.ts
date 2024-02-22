export type CommandType = "FOR" | "WHILE" | "IF" | "ELSE" | "SET" | "END";

//functions of either of these types aren't required on front end hence unimplemented
export interface FunctionCode {
  commandType: CommandType;
  number: number;
  linkedCommands?: number[];
  params?: string[];
}

export interface Schedule {
  id: string;
  name: string;
  isPublic: boolean;
  isActive: boolean;
  ratings: number[]; //was just one value, but instead should be a computed value
  triggers: Trigger[];
  code: FunctionCode[];
  customVars?: string[];
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
