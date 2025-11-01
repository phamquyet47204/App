export const GradeType = {
  MIDTERM: 'midterm',
  FINAL: 'final',
  ASSIGNMENT: 'assignment',
  QUIZ: 'quiz',
  PROJECT: 'project',
  ATTENDANCE: 'attendance'
};

export const GradeStatus = {
  PENDING: 'pending',
  GRADED: 'graded',
  RELEASED: 'released'
};

export class Grade {
  constructor({
    id,
    gradeId,
    studentId,
    subjectCode,
    subjectName,
    subject,
    courseClass,
    semester,
    gradeType,
    assignmentScore,
    midtermScore,
    finalScore,
    averageScore,
    letterGrade,
    gradePoint,
    isPassed,
    score,
    maxScore,
    weight,
    status = GradeStatus.PENDING,
    teacherName,
    gradedAt,
    description,
    createdAt,
    updatedAt
  }) {
    this.id = id;
    this.gradeId = gradeId;
    this.studentId = studentId;
    this.subjectCode = subjectCode;
    this.subjectName = subjectName || subject;
    this.courseClass = courseClass;
    this.semester = semester;
    this.gradeType = gradeType;
    this.assignmentScore = assignmentScore;
    this.midtermScore = midtermScore;
    this.finalScore = finalScore;
    this.averageScore = averageScore;
    this.letterGrade = letterGrade;
    this.gradePoint = gradePoint;
    this.isPassed = isPassed;
    this.score = score;
    this.maxScore = maxScore;
    this.weight = weight;
    this.status = status;
    this.teacherName = teacherName;
    this.gradedAt = gradedAt;
    this.description = description;
    this.createdAt = createdAt;
    this.updatedAt = updatedAt;
  }

  getPercentage() {
    if (this.averageScore !== undefined) {
      return this.averageScore;
    }
    return this.maxScore > 0 ? (this.score / this.maxScore) * 100 : 0;
  }

  getLetterGrade() {
    if (this.letterGrade) {
      return this.letterGrade;
    }
    const percentage = this.getPercentage();
    if (percentage >= 90) return 'A';
    if (percentage >= 80) return 'B';
    if (percentage >= 70) return 'C';
    if (percentage >= 60) return 'D';
    return 'F';
  }
}

export class SubjectGrade {
  constructor({
    subjectCode,
    subjectName,
    grades = [],
    finalGrade,
    letterGrade,
    credits,
    semester,
    year
  }) {
    this.subjectCode = subjectCode;
    this.subjectName = subjectName;
    this.grades = grades;
    this.finalGrade = finalGrade;
    this.letterGrade = letterGrade;
    this.credits = credits;
    this.semester = semester;
    this.year = year;
  }
}
