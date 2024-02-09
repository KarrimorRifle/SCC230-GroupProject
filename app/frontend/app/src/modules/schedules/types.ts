
type CommandType = 'FOR' | 'WHILE' | "IF" | "OTHERWISE" | "SET" | "GET" | "END";

//functions of either of these types aren't required on front end hence unimplemented
interface FunctionCode{
  commandType: CommandType,
  number: number,
  linkedCommands?: FunctionCode[],
  params?: string[]
}

interface Schedule{
  id: string,
  name: string,
  isPublic: boolean,
  isActive: boolean,
  ratings: number[],//was just one value, but instead should be a computed value
  triggers: Trigger[],
  code: FunctionCode[],
}

interface Trigger{
  id: string,
  data: Record<string, string[]>, //deviceID: data
}

interface Device{
  id: string,
  name: string,
  isActive: boolean,
  data: Record<string,any>,
}