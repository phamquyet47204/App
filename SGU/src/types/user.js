export const UserRole = {
  STUDENT: 'student',
  ADMIN: 'admin',
  TEACHER: 'teacher'
};

export const UserStatus = {
  ACTIVE: 'active',
  INACTIVE: 'inactive',
  SUSPENDED: 'suspended'
};

export class User {
  constructor({
    id,
    username,
    studentId,
    fullName,
    full_name,
    email,
    phone,
    dateOfBirth,
    address,
    major,
    className,
    year,
    role = UserRole.STUDENT,
    user_type = 'student',
    status = UserStatus.ACTIVE,
    avatar,
    createdAt,
    updatedAt
  }) {
    this.id = id;
    this.username = username;
    this.studentId = studentId;
    this.fullName = fullName || full_name;
    this.email = email;
    this.phone = phone;
    this.dateOfBirth = dateOfBirth;
    this.address = address;
    this.major = major;
    this.class = className;
    this.year = year;
    this.role = role;
    this.user_type = user_type;
    this.status = status;
    this.avatar = avatar;
    this.createdAt = createdAt;
    this.updatedAt = updatedAt;
  }
}

export class AuthStorage {
  static isLoggedIn() {
    return localStorage.getItem('sgu_user') !== null;
  }

  static getCurrentUser() {
    const userData = localStorage.getItem('sgu_user');
    return userData ? JSON.parse(userData) : null;
  }

  static setCurrentUser(user) {
    localStorage.setItem('sgu_user', JSON.stringify(user));
  }

  static logout() {
    localStorage.removeItem('sgu_user');
  }
}
