// File: static/CNPM2/js/import_logic.js

let itemCount = 1;
const itemContainer = document.getElementById("items-container");

// Hàm tạo thêm dòng sản phẩm mới
function addItemRow() {
  const firstRow = itemContainer.querySelector(".item-row");
  if (!firstRow) return;

  const newRow = document.createElement("div");
  newRow.className = "item-row";
  newRow.innerHTML = firstRow.innerHTML;

  // Reset giá trị cho các input/select trong dòng mới
  const inputs = newRow.querySelectorAll("input, select");
  inputs.forEach((input) => {
    // Reset giá trị
    if (input.type === "text") input.value = "";
    if (input.type === "number")
      input.value = input.getAttribute("placeholder") === "Giá nhập" ? "" : 1;

    // Đảm bảo tất cả các SELECT (sản phẩm, category) được reset về rỗng
    if (input.tagName === "SELECT") input.value = "";

    // Đảm bảo các input được kích hoạt lại (không bị disabled)
    input.disabled = false;
    if (input.classList.contains("new-item-name-input")) {
      input.placeholder = "Hoặc nhập tên sản phẩm mới";
    }

    // Đảm bảo Ngành hàng (select) là required mặc định
    if (input.name === "category_id") {
      input.required = true;
    }
  });

  itemContainer.appendChild(newRow);
  itemCount++;
}

// Hàm xóa dòng sản phẩm (Giữ nguyên)
function removeItemRow(buttonElement) {
  if (itemContainer.childElementCount > 1) {
    buttonElement.closest(".item-row").remove();
    itemCount--;
  } else {
    alert("Phiếu nhập phải có ít nhất một sản phẩm.");
  }
}

// ----------------------------------------------------------------------
// LOGIC BÙ TRỪ VÀ BẮT BUỘC CHỌN CATEGORY KHI TẠO MỚI
// ----------------------------------------------------------------------

// Xử lý khi người dùng CHỌN một sản phẩm đã có
function handleItemChange(selectElement) {
  const row = selectElement.closest(".item-row");
  const newItemInput = row.querySelector(".new-item-name-input");
  // Lấy selector Ngành hàng (select)
  const categorySelector = row.querySelector(".category-selector");

  if (selectElement.value) {
    // Nếu đã chọn sản phẩm cũ:
    newItemInput.value = "";
    newItemInput.disabled = true; // Vô hiệu hóa ô nhập tên mới

    // Category KHÔNG cần required (vì sản phẩm đã có Category)
    categorySelector.required = false;
    categorySelector.disabled = true; // Vô hiệu hóa ô chọn Category (Tránh thay đổi Category cho sản phẩm cũ)
  } else {
    // Nếu không chọn gì (chọn tạo mới):
    newItemInput.disabled = false;

    // Category BẮT BUỘC required (vì tạo sản phẩm mới phải chọn Ngành hàng)
    categorySelector.required = true;
    categorySelector.disabled = false; // Kích hoạt ô chọn Category
  }
}

// Xử lý khi người dùng NHẬP TÊN SẢN PHẨM MỚI
function handleNewItemInput(inputElement) {
  const row = inputElement.closest(".item-row");
  const itemSelector = row.querySelector(".item-selector");

  if (inputElement.value.trim() !== "") {
    // Nếu đã nhập tên mới, buộc ô chọn sản phẩm cũ về giá trị rỗng (không chọn)
    itemSelector.value = "";
  }
  // Sau đó, kích hoạt lại hàm handleItemChange để vô hiệu hóa/kích hoạt đúng
  handleItemChange(itemSelector);
}
