export const PaymentStatus = {
  UNPAID: 'unpaid',
  PARTIAL: 'partial',
  PAID: 'paid',
  OVERDUE: 'overdue'
};

export class TuitionFee {
  constructor({
    tuitionFeeId,
    student,
    studentId,
    semester,
    semesterId,
    totalCredits,
    feePerCredit,
    totalAmount,
    paidAmount,
    paymentStatus = PaymentStatus.UNPAID,
    dueDate,
    createdAt,
    updatedAt
  }) {
    this.tuitionFeeId = tuitionFeeId;
    this.student = student;
    this.studentId = studentId;
    this.semester = semester;
    this.semesterId = semesterId;
    this.totalCredits = totalCredits;
    this.feePerCredit = feePerCredit;
    this.totalAmount = totalAmount;
    this.paidAmount = paidAmount;
    this.paymentStatus = paymentStatus;
    this.dueDate = dueDate;
    this.createdAt = createdAt;
    this.updatedAt = updatedAt;
  }

  getRemainingAmount() {
    return this.totalAmount - this.paidAmount;
  }

  getPaymentPercentage() {
    return this.totalAmount > 0 ? (this.paidAmount / this.totalAmount) * 100 : 0;
  }

  isPaid() {
    return this.paymentStatus === PaymentStatus.PAID;
  }

  isOverdue() {
    if (this.paymentStatus === PaymentStatus.OVERDUE) {
      return true;
    }
    return this.dueDate && new Date() > new Date(this.dueDate) && !this.isPaid();
  }

  isPartiallyPaid() {
    return this.paymentStatus === PaymentStatus.PARTIAL;
  }
}
