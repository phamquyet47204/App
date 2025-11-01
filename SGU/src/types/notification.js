export const NotificationType = {
  INFO: 'info',
  WARNING: 'warning',
  SUCCESS: 'success',
  ERROR: 'error',
  ANNOUNCEMENT: 'announcement'
};

export const NotificationStatus = {
  UNREAD: 'unread',
  READ: 'read',
  ARCHIVED: 'archived'
};

export class Notification {
  constructor({
    id,
    notificationId,
    title,
    message,
    content,
    type = NotificationType.INFO,
    notificationType = 'general',
    priority = 1,
    status = NotificationStatus.UNREAD,
    isImportant = false,
    targetUserId,
    relatedId,
    relatedType,
    createdAt,
    deliveredAt,
    readAt,
    expiresAt
  }) {
    this.id = id || notificationId;
    this.title = title;
    this.message = message || content;
    this.type = type;
    this.notificationType = notificationType;
    this.priority = priority;
    this.status = status;
    this.isImportant = isImportant;
    this.targetUserId = targetUserId;
    this.relatedId = relatedId;
    this.relatedType = relatedType;
    this.createdAt = createdAt;
    this.deliveredAt = deliveredAt;
    this.readAt = readAt;
    this.expiresAt = expiresAt;
  }

  isExpired() {
    return this.expiresAt && new Date() > new Date(this.expiresAt);
  }

  markAsRead() {
    this.status = NotificationStatus.READ;
    this.readAt = new Date();
  }

  archive() {
    this.status = NotificationStatus.ARCHIVED;
  }
}
