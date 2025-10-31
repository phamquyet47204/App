export class CourseClass {
  constructor({
    courseClassId,
    courseCode,
    courseName,
    subject,
    teacher,
    semester,
    room,
    maxStudents,
    currentStudents,
    credits,
    availableSlots
  }) {
    this.courseClassId = courseClassId;
    this.courseCode = courseCode;
    this.courseName = courseName;
    this.subject = subject;
    this.teacher = teacher;
    this.semester = semester;
    this.room = room;
    this.maxStudents = maxStudents;
    this.currentStudents = currentStudents;
    this.credits = credits;
    this.availableSlots = availableSlots;
  }

  getEnrollmentPercentage() {
    return this.maxStudents > 0 ? (this.currentStudents / this.maxStudents) * 100 : 0;
  }

  isFull() {
    return this.currentStudents >= this.maxStudents;
  }
}

export class Prerequisite {
  constructor({
    subjectCode,
    subjectName
  }) {
    this.subjectCode = subjectCode;
    this.subjectName = subjectName;
  }
}

export class PrerequisiteCheck {
  constructor({
    canRegister,
    missingPrerequisites = []
  }) {
    this.canRegister = canRegister;
    this.missingPrerequisites = missingPrerequisites;
  }
}
