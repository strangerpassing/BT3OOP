# Mã số sinh viên: 202418898
# Họ và tên: Nguyễn Trung Hiếu
class Employee:
    # Biến lớp (class variable) để theo dõi các ID đã tồn tại, đảm bảo tính duy nhất
    _existing_ids = set()

    def __init__(self, id="UNKNOWN", fullName="Unnamed Employee", baseSalary=0):
        # Ràng buộc dữ liệu
        if not id or not fullName:
            raise ValueError("Lỗi: Mã nhân viên và họ tên không được rỗng.")
        if baseSalary < 0:
            raise ValueError("Lỗi: Lương cơ bản không được âm.")
        if id != "UNKNOWN" and id in Employee._existing_ids:
            raise ValueError(f"Lỗi: Nhân viên với mã số '{id}' đã tồn tại.")

        self.id = id
        self.fullName = fullName
        self.baseSalary = baseSalary
        
        # Thêm ID vào danh sách đã tồn tại nếu không phải là giá trị mặc định
        if id != "UNKNOWN":
            Employee._existing_ids.add(id)

    def increaseSalarybyamount(self, amount):
        if amount > 0:
            self.baseSalary += amount

    def increaseSalarybypercentage(self, value, confirm, amount=0):
        # Nếu confirm == True thì tăng theo phần trăm, nếu False thì gọi hàm tăng theo số tiền nhất định
        if confirm:
            if value > 0:
                self.baseSalary += self.baseSalary * (value / 100.0)
        else:
            self.increaseSalarybyamount(amount)

    def calculateMonthlyCost(self):
        # Hàm tính toán chi phí (được xem như virtual method trong Python)
        return self.baseSalary

    def displayInfo(self):
        print(f"[{self.id}] Nhân viên: {self.fullName} | Lương cơ bản: {self.baseSalary}")

    def __del__(self):
        # Destructor thông báo vòng đời
        print(f"[Hủy] Đối tượng Employee: {self.fullName} (ID: {self.id})")
        # Xóa ID khỏi bộ nhớ khi đối tượng bị hủy để tái sử dụng
        if hasattr(self, 'id') and self.id in Employee._existing_ids:
            Employee._existing_ids.discard(self.id)


class SoftwareEngineer(Employee):
    def __init__(self, id, fullName, baseSalary=0, primaryLanguage=None, technicalAllowance=0):
        # Xử lý linh hoạt số lượng tham số để mô phỏng tính đa hình (overloading constructors)
        if primaryLanguage is None:
            # Trường hợp gọi 3 tham số: id, fullName, primaryLanguage
            actual_language = baseSalary 
            super().__init__(id, fullName, 0)
            self.primaryLanguage = actual_language
            self.technicalAllowance = 0
        else:
            # Trường hợp gọi 5 tham số
            super().__init__(id, fullName, baseSalary)
            self.primaryLanguage = primaryLanguage
            self.technicalAllowance = technicalAllowance

        if not self.primaryLanguage:
            raise ValueError("Lỗi: Ngôn ngữ lập trình chính không được rỗng.")
        if getattr(self, 'technicalAllowance', 0) < 0:
            raise ValueError("Lỗi: Phụ cấp kỹ thuật không được âm.")

    def calculateMonthlyCost(self):
        # Ghi đè (override) hàm tính tổng chi phí (lương cơ bản + phụ cấp)
        return self.baseSalary + self.technicalAllowance

    def displayInfo(self):
        # Ghi đè hàm hiển thị
        print(f"[{self.id}] Kỹ sư: {self.fullName} | Ngôn ngữ: {self.primaryLanguage} | Lương: {self.baseSalary} | Phụ cấp: {self.technicalAllowance}")

    def __del__(self):
        print(f"[Hủy] Đối tượng SoftwareEngineer: {self.fullName} (ID: {self.id})")
        # Mặc định Python tự gọi constructor của lớp cha hoặc ta có thể để trống vì super().__del__ sẽ được kích hoạt ngầm nếu dùng biến phù hợp


class ProjectTeam:
    def __init__(self, projectCode, projectName, leader=None):
        self.projectCode = projectCode
        self.projectName = projectName
        self.members = []  # Danh sách liên kết không sở hữu
        self.leader = None # Liên kết không sở hữu đến trưởng nhóm

        # Nếu truyền trưởng nhóm khi khởi tạo, tự động thiết lập và thêm vào nhóm
        if leader is not None:
            self.changeLeader(leader)

    def contains(self, employeeId):
        # Kiểm tra xem nhân sự có trong nhóm hay chưa
        return any(member.id == employeeId for member in self.members)

    def addMember(self, employee):
        # Khi thêm nhân viên mới, không được trùng nhân sự
        if not self.contains(employee.id):
            self.members.append(employee)
        else:
            print(f"Nhân sự '{employee.fullName}' (ID: {employee.id}) đã có trong nhóm dự án {self.projectName}.")

    def leadership(self, employee, makeLeader):
        # Thêm vào nhóm (addMember đã tự kiểm tra trùng), làm trưởng nhóm nếu makeLeader = True
        self.addMember(employee)
        if makeLeader:
            self.leader = employee

    def changeLeader(self, employee):
        # Trưởng nhóm mới phải được thêm vào nhóm nếu chưa phải thành viên
        self.addMember(employee)
        # Trưởng nhóm cũ vẫn nằm trong self.members do ta chỉ trỏ lại self.leader
        self.leader = employee

    def removeMember(self, employee_id):
        # Không được xóa trưởng nhóm khi chưa chọn trưởng nhóm thay thế
        if self.leader and self.leader.id == employee_id:
            raise ValueError("Lỗi: Không được xóa trưởng nhóm khi chưa chọn trưởng nhóm thay thế!")
        
        # Xóa nhân viên ra khỏi danh sách
        self.members = [m for m in self.members if m.id != employee_id]

    def calculateTotalMonthlyCost(self):
        # Tính chi phí dựa trên virtual method `calculateMonthlyCost` của từng nhân viên
        return sum(member.calculateMonthlyCost() for member in self.members)

    def displayTeam(self):
        print(f"\n--- DỰ ÁN: {self.projectName} ({self.projectCode}) ---")
        leader_name = self.leader.fullName if self.leader else "Chưa có"
        print(f"Trưởng nhóm: {leader_name}")
        print("Thành viên:")
        for m in self.members:
            m.displayInfo()
        print(f"Tổng chi phí dự án: {self.calculateTotalMonthlyCost()}")
        print("---------------------------------")

    def __del__(self):
        print(f"[Hủy] Đối tượng ProjectTeam: {self.projectName}. Dọn dẹp liên kết nội bộ...")
        # Chỉ dọn dẹp (xóa) cấu trúc danh sách liên kết nội bộ, không hủy trực tiếp các đối tượng Employee
        self.members.clear()
        self.leader = None

e3 = SoftwareEngineer("20010001", "John Doe", "C")
e4 = SoftwareEngineer("19920001", "Tails", 20000000, "C", 2500000)
e1 = Employee("20010002", "Amy", 12000000)
e2 = SoftwareEngineer("19910002", "Ivo", 21000000, "C", 50000000)
e3.increaseSalarybyamount(7500000)
e3.increaseSalarybypercentage(137.5, True)
g1 = ProjectTeam("P1", "Zeus")
g1.addMember(e3)
g1.addMember(e1)
g1.leadership(e2, True)
g2 = ProjectTeam("P2", "Artemis", e4)
g2.leadership(e4, True)
g2.addMember(e1)
g2.addMember(e3)
remainings = []
for i in g2.members:
    remainings.append(i)
g2.__del__()
for j in range(0,len(remainings),1):
    remainings[j].displayInfo()