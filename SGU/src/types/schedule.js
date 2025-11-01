export const ScheduleStatus = {
  SCHEDULED: 'scheduled',
  ONGOING: 'ongoing',
  COMPLETED: 'completed',
  CANCELLED: 'cancelled'
};

export const DayOfWeek = {
  MONDAY: 'monday',
  TUESDAY: 'tuesday',
  WEDNESDAY: 'wednesday',
  THURSDAY: 'thursday',
  FRIDAY: 'friday',
  SATURDAY: 'saturday',
  SUNDAY: 'sunday'
};

export class Schedule {
  constructor({
    id,
    subjectCode,
    subjectName,
    teacherName,
    room,
    dayOfWeek,
    startTime,
    endTime,
    date,
    status = ScheduleStatus.SCHEDULED,
    description,
    createdAt,
    updatedAt
  }) {
    this.id = id;
    this.subjectCode = subjectCode;
    this.subjectName = subjectName;
    this.teacherName = teacherName;
    this.room = room;
    this.dayOfWeek = dayOfWeek;
    this.startTime = startTime;
    this.endTime = endTime;
    this.date = date;
    this.status = status;
    this.description = description;
    this.createdAt = createdAt;
    this.updatedAt = updatedAt;
  }
}

export class ClassSchedule {
  constructor({
    id,
    className,
    schedules = [],
    semester,
    year,
    createdAt,
    updatedAt
  }) {
    this.id = id;
    this.className = className;
    this.schedules = schedules;
    this.semester = semester;
    this.year = year;
    this.createdAt = createdAt;
    this.updatedAt = updatedAt;
  }
}
