from app.models import app, db, Computer, HardDriveType
from flask import request, jsonify


@app.route("/")
def index():
    return "<h1>Computer Application Is Running</h1>"


@app.route("/computer/<int:computer_id>", methods=["GET"])
def get_computer(computer_id):
    computer = Computer.query.get_or_404(computer_id)
    return jsonify(
        {
            "computer": {
                "id": computer.id,
                "hard_drive_type": computer.hard_drive_type.value,
                "processor": computer.processor,
                "ram_amount": computer.ram_amount,
                "maximum_ram": computer.maximum_ram,
                "hard_drive_space": computer.hard_drive_space,
                "form_factor": computer.form_factor,
            }
        }
    )


@app.route("/computers", methods=["GET"])
def get_computers():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    computers = Computer.query.paginate(page=page, per_page=per_page, error_out=True)

    return jsonify(
        {
            "computers": [
                {
                    "id": computer.id,
                    "hard_drive_type": computer.hard_drive_type.value,
                    "processor": computer.processor,
                    "ram_amount": computer.ram_amount,
                    "maximum_ram": computer.maximum_ram,
                    "hard_drive_space": computer.hard_drive_space,
                    "form_factor": computer.form_factor,
                }
                for computer in computers.items
            ],
            "total": computers.total,
            "pages": computers.pages,
            "current_page": computers.page,
            "per_page": computers.per_page,
        }
    )


@app.route("/computer", methods=["POST"])
def add_computer():
    data = request.get_json()
    new_computer = Computer(
        hard_drive_type=HardDriveType[data["hard_drive_type"]],
        processor=data["processor"],
        ram_amount=data["ram_amount"],
        maximum_ram=data["maximum_ram"],
        hard_drive_space=data["hard_drive_space"],
        form_factor=data["form_factor"],
    )
    db.session.add(new_computer)
    db.session.commit()
    return jsonify({"message": "Computer added successfully"}), 201


@app.route("/computer/<int:computer_id>", methods=["PUT"])
def edit_computer(computer_id):
    data = request.get_json()
    computer = Computer.query.get_or_404(computer_id)

    if "hard_drive_type" in data:
        computer.hard_drive_type = HardDriveType[data["hard_drive_type"]]
    computer.processor = data.get("processor", computer.processor)
    computer.ram_amount = data.get("ram_amount", computer.ram_amount)
    computer.maximum_ram = data.get("maximum_ram", computer.maximum_ram)
    computer.hard_drive_space = data.get("hard_drive_space", computer.hard_drive_space)
    computer.form_factor = data.get("form_factor", computer.form_factor)

    db.session.commit()
    return jsonify({"message": "Computer updated successfully"}), 200


@app.route("/computer/<int:computer_id>", methods=["DELETE"])
def delete_computer(computer_id):
    computer = Computer.query.get_or_404(computer_id)
    db.session.delete(computer)
    db.session.commit()
    return jsonify({"message": "Computer deleted successfully"}), 200
