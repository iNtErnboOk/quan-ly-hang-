function openModal(mode) {
  document.getElementById("modalOverlay").style.display = "flex";
  document.getElementById("itemMode").value = mode;
  document.getElementById("itemForm").action = "/add/"; // Đưa form về action tạo mới mặc định

  let title = document.getElementById("modalTitle");
  let submitBtn = document.getElementById("submitBtn");

  if (mode === "PRODUCT") {
    title.innerText = "Thêm Sản Phẩm Mới";
    submitBtn.style.backgroundColor = "#28a745";
  } else if (mode === "IMPORT") {
    title.innerText = "Tạo Phiếu Nhập Kho";
    submitBtn.style.backgroundColor = "#fd7e14";
  } else {
    title.innerText = "Tạo Phiếu Xuất Kho";
    submitBtn.style.backgroundColor = "#0056b3";
  }

  // Tự động random SKU khi tạo mới
  document.getElementById("skuInput").value =
    "SKU-" + Math.floor(10000 + Math.random() * 90000);
  document.getElementById("nameInput").value = "";
}

function openEditModal(id, name, sku, category, price, quantity, mode) {
  document.getElementById("modalOverlay").style.display = "flex";
  document.getElementById("modalTitle").innerText = "Chỉnh sửa thông tin"; //

  // Đổi action form sang URL update trong CSDL
  document.getElementById("itemForm").action = "/update/" + id + "/";

  document.getElementById("nameInput").value = name;
  document.getElementById("skuInput").value = sku;
  document.getElementById("categoryInput").value = category;
  document.getElementById("priceInput").value = price;
  document.getElementById("quantityInput").value = quantity;
  document.getElementById("itemMode").value = mode;

  document.getElementById("submitBtn").innerText = "Cập nhật ngay";
  document.getElementById("submitBtn").style.backgroundColor = "#28a745";
}

// Hàm Đóng Modal
function closeModal() {
  document.getElementById("modalOverlay").style.display = "none";
}

window.onclick = function (event) {
  let modal = document.getElementById("modalOverlay");
  if (event.target == modal) closeModal();
};
document.addEventListener("DOMContentLoaded", function () {
  // Tìm tất cả các thẻ có class là product-price
  const priceElements = document.querySelectorAll(".product-price");

  priceElements.forEach((el) => {
    let price = el.innerText.trim();

    // Chuyển đổi số thành định dạng có dấu chấm phân cách
    if (!isNaN(price) && price !== "") {
      let formattedPrice = Number(price).toLocaleString("vi-VN");
      el.innerText = formattedPrice + "đ";
    }
  });
});
