export const DocumentRequestStatus = {
  PENDING: 'pending',
  APPROVED: 'approved',
  REJECTED: 'rejected',
  PROCESSING: 'processing',
  COMPLETED: 'completed'
};

export class DocumentRequest {
  constructor({
    requestId,
    documentType,
    documentTypeId,
    semester,
    semesterId,
    requestDate,
    purpose,
    status = DocumentRequestStatus.PENDING,
    studentIds = [],
    createdAt,
    updatedAt
  }) {
    this.requestId = requestId;
    this.documentType = documentType;
    this.documentTypeId = documentTypeId;
    this.semester = semester;
    this.semesterId = semesterId;
    this.requestDate = requestDate;
    this.purpose = purpose;
    this.status = status;
    this.studentIds = studentIds;
    this.createdAt = createdAt;
    this.updatedAt = updatedAt;
  }

  isPending() {
    return this.status === DocumentRequestStatus.PENDING;
  }

  isApproved() {
    return this.status === DocumentRequestStatus.APPROVED;
  }

  isRejected() {
    return this.status === DocumentRequestStatus.REJECTED;
  }

  isCompleted() {
    return this.status === DocumentRequestStatus.COMPLETED;
  }
}
