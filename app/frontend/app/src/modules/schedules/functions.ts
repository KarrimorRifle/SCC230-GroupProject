import { Schedule } from "./types";
export const getSchedules = async (): Promise<Schedule[]> => {
  //use user details to return schedules
  return [
    <Schedule>{
      id: "01",
      name: "name1",
      isPublic: false,
      isActive: false,
      ratings: [],
      triggers: [],
      code: [],
    },
    <Schedule>{
      id: "02",
      name: "name2",
      isPublic: false,
      isActive: false,
      ratings: [],
      triggers: [],
      code: [],
    },
    <Schedule>{
      id: "03",
      name: "name3",
      isPublic: false,
      isActive: false,
      ratings: [],
      triggers: [],
      code: [],
    },
    <Schedule>{
      id: "04",
      name: "name4",
      isPublic: false,
      isActive: false,
      ratings: [],
      triggers: [],
      code: [],
    },
  ];
};

export const getScheduleByID = async (id: string): Promise<Schedule> => {
  return <Schedule>{
    id: "01",
    name: "name1",
    isPublic: false,
    isActive: false,
    ratings: [],
    triggers: [],
    code: [],
  };
};
