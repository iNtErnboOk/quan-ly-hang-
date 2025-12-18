function openModal(mode) {
  const modal = document.getElementById("modalOverlay");
  const title = document.getElementById("modalTitle");
  const form = document.getElementById("itemForm");
  const submitBtn = document.getElementById("submitBtn");
  const modeInput = document.getElementById("itemMode");

  modal.style.display = "flex";
  modeInput.value = mode;

  // Dùng đường dẫn trực tiếp, tuyệt đối không dùng {% url %} trong JS tĩnh
  form.action = "/add/";
  submitBtn.innerText = "Tạo Sản Phẩm";

  if (mode === "PRODUCT") {
    title.innerText = "Thêm Sản Phẩm Mới";
    submitBtn.style.backgroundColor = "#28a745";
  }

  // Tự động sinh SKU ngẫu nhiên
  document.getElementById("skuInput").value =
    "SKU-" + Math.floor(10000 + Math.random() * 90000);
  document.getElementById("nameInput").value = "";
  document.getElementById("priceInput").value = "0";
  document.getElementById("quantityInput").value = "1";
}

function openEditModal(id, name, sku, category, price, quantity, mode) {
  document.getElementById("modalOverlay").style.display = "flex";
  document.getElementById("modalTitle").innerText = "Chỉnh sửa thông tin";

  // Gán đường dẫn update trực tiếp
  document.getElementById("itemForm").action = "/update/" + id + "/";

  document.getElementById("nameInput").value = name;
  document.getElementById("skuInput").value = sku;
  document.getElementById("categoryInput").value = category;
  document.getElementById("priceInput").value = price;
  document.getElementById("quantityInput").value = quantity;
  document.getElementById("itemMode").value = mode;

  const submitBtn = document.getElementById("submitBtn");
  submitBtn.innerText = "Cập nhật ngay";
  submitBtn.style.backgroundColor = "#28a745";
}

function closeModal() {
  document.getElementById("modalOverlay").style.display = "none";
  document.getElementById("itemForm").reset();
}

// Xử lý đóng modal khi click ra ngoài
window.onclick = function (event) {
  let modal = document.getElementById("modalOverlay");
  let detailModal = document.getElementById("detailModalOverlay");
  if (event.target == modal) closeModal();
  if (event.target == detailModal) detailModal.style.display = "none";
};

// Định dạng giá tiền cho danh sách ngoài màn hình chính
document.addEventListener("DOMContentLoaded", function () {
  const priceElements = document.querySelectorAll(".product-price");
  priceElements.forEach((el) => {
    let price = el.innerText.replace(/[^\d]/g, ""); // Xóa ký tự không phải số
    if (price !== "") {
      el.innerText = new Intl.NumberFormat("vi-VN").format(price) + "đ";
    }
  });
});

// Hiển thị chi tiết sản phẩm và giá nhập
function showProductDetail(id) {
  fetch(`/product-detail-api/${id}/`)
    .then((res) => res.json())
    .then((data) => {
      document.getElementById("detName").innerText = data.name;
      document.getElementById("detSKU").innerText = data.sku;
      document.getElementById("detCat").innerText = data.category;
      document.getElementById("detPrice").innerText = data.price;

      const importPriceSpan = document.getElementById("detImportPrice");
      if (data.cost_price) {
        const formatted = new Intl.NumberFormat("vi-VN").format(
          data.cost_price
        );
        importPriceSpan.innerText = formatted + "đ";
      } else {
        importPriceSpan.innerText = "0đ";
      }

      document.getElementById("detQty").innerText = data.quantity;
      document.getElementById("detImage").src = data.image ? data.image : "";
      document.getElementById("detImportHistory").innerHTML = data.import_html;
      document.getElementById("detExportHistory").innerHTML = data.export_html;
      document.getElementById("detailModalOverlay").style.display = "flex";
    });
}
