$(document).ready(function () {
  // Disease page mapping
  const DISEASE_PAGE_MAPPING = {
    "bacterial leaf blight": "leafblight.html",
    "bacterial leaf streak": "leafstreak.html",
    "bacterial panicle blight": "panicle.html",
    blast: "blast.html",
    "brown spot": "brown.html",
    "dead heart": "DeadHeart.html",
    "downy mildew": "downy.html",
    hispa: "hispa.html",
    healthy: "guide.html",
    tungro: "tungro.html",
    unknown: "unknown_disease.html",
  };

  // Confidence thresholds
  const CONFIDENCE_THRESHOLDS = {
    high: 0.75,
    medium: 0.5,
    low: 0.3,
  };

  // Initialize elements
  $(".image-section").hide();
  $(".loader").hide();
  $("#result-container").hide();
  $("#btn-report").hide();
  $("#btn-clear").hide();
  $("#invalid-image-alert").hide();

  // Handle file upload
  $("#imageUpload").change(function () {
    if (this.files && this.files[0]) {
      var reader = new FileReader();
      reader.onload = function (e) {
        $("#imagePreview").css(
          "background-image",
          "url(" + e.target.result + ")"
        );
        $(".image-section").show();
        $("#btn-predict").show();
        $("#result-container").hide();
        $("#invalid-image-alert").hide();
        $("#btn-clear").show();
      };
      reader.readAsDataURL(this.files[0]);
    }
  });

  // Handle prediction button click
  $("#btn-predict").click(function () {
    var formData = new FormData($("#upload-file")[0]);
    $(this).prop("disabled", true);
    $(".loader").show();
    $("#result-container").hide();
    $("#btn-report").hide();
    $("#invalid-image-alert").hide();

    $.ajax({
      type: "POST",
      url: "/predict",
      data: formData,
      contentType: false,
      cache: false,
      processData: false,
      success: function (response) {
        $(".loader").hide();
        if (response.error) {
          showError(response.error);
        } else {
          displayResults(response);
        }
        $("#btn-predict").prop("disabled", false);
      },
      error: function (xhr) {
        showError(xhr.responseJSON?.error || "Server error");
        $("#btn-predict").prop("disabled", false);
      },
    });
  });

  // Display results function
  function displayResults(response) {
    console.log("Raw response:", response);

    // Always show original image
    $("#original-image").attr("src", response.image_url);

    // Set confidence display
    const confidencePercent = Math.round(response.confidence * 100);
    $("#confidence-percent").text(`${confidencePercent}%`);
    $("#confidence-bar").css("width", `${confidencePercent}%`);

    // Update confidence UI
    updateConfidenceUI(response.confidence);

    // Handle different cases
    if (response.class_name === "invalid") {
      handleInvalidImage(response);
    } else {
      // Show heatmap for valid images
      $("#gradcam-image").attr("src", response.gradcam_url);

      if (
        response.class_name === "unknown" ||
        response.confidence < CONFIDENCE_THRESHOLDS.medium
      ) {
        handleUnknownDisease(response, confidencePercent);
      } else {
        handleKnownDisease(response);
      }
    }

    // Show results container
    $("#result-container").hide().removeClass("d-none").fadeIn(500);
    $("html, body").animate(
      { scrollTop: $("#result-container").offset().top - 20 },
      500
    );
  }

  function resetImageLayout() {
    // Reset both columns to their original state
    $("#original-col").removeClass("col-12").addClass("col-md-6").show();
    $("#gradcam-col").removeClass("d-none").addClass("col-md-6").show();

    // Force browser to recalculate layout
    $(".image-row").hide().show();
  }

  function updateConfidenceUI(confidence) {
    const $bar = $("#confidence-bar");
    const $label = $("#confidence-label");

    if (confidence >= CONFIDENCE_THRESHOLDS.high) {
      $bar.removeClass("bg-warning bg-danger").addClass("bg-success");
      $label
        .text("High confidence")
        .removeClass("text-warning text-danger")
        .addClass("text-success");
    } else if (confidence >= CONFIDENCE_THRESHOLDS.medium) {
      $bar.removeClass("bg-success bg-danger").addClass("bg-warning");
      $label
        .text("Moderate confidence")
        .removeClass("text-success text-danger")
        .addClass("text-warning");
    } else {
      $bar.removeClass("bg-success bg-warning").addClass("bg-danger");
      $label
        .text("Low confidence")
        .removeClass("text-success text-warning")
        .addClass("text-danger");
    }
  }

  function handleInvalidImage(response) {
    $("#invalid-image-alert").show();

    // Hide heatmap column completely
    $("#gradcam-col").addClass("d-none");

    // Expand original image to full width
    $("#original-col").removeClass("col-md-6").addClass("col-12");

    $("#prediction-text").html(
      '<span class="text-danger">Invalid Image</span>'
    );
    $("#unknown-disease-alert").hide();
    $("#btn-details").hide();
    $("#btn-report").hide();
  }

  function handleUnknownDisease(response, confidencePercent) {
    $("#prediction-text").html(`
        ${response.prediction} 
        <span class="badge bg-danger">Low Confidence</span>
      `);

    $("#unknown-disease-alert")
      .html(
        `
        <i class="fas fa-exclamation-triangle me-2"></i>
        <strong>Low Confidence Detection (${confidencePercent}%):</strong> 
        This might be an unknown disease.
        <button id="btn-report" class="btn btn-sm btn-warning ms-2">
          <i class="fas fa-flag me-1"></i> Report
        </button>
      `
      )
      .show();

    $("#btn-details").hide();
    $("#btn-report")
      .show()
      .off("click")
      .click(function () {
        prepareReportModal(response);
      });
  }

  function handleKnownDisease(response) {
    $("#prediction-text").text(response.prediction);
    $("#unknown-disease-alert").hide();
    $("#btn-details").show();
    $("#btn-report").hide();
  }

  // Show error message
  function showError(message) {
    $("#result").removeClass("alert-success").addClass("alert-danger");
    $("#result")
      .find("span")
      .text("Error: " + message);
    $("#result").fadeIn();
    $(".loader").hide();
  }

  // Prepare report modal with data
  function prepareReportModal(response) {
    $("#reportImagePreview").attr("src", response.image_url);
    $("#reportModal").modal("show");
  }

  // Image zoom functionality
  $(document).on("click", ".img-fluid", function () {
    const src = $(this).attr("src");
    const modal = `
      <div class="modal fade" id="imageModal" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered modal-xl">
          <div class="modal-content">
            <div class="modal-body text-center p-0">
              <img src="${src}" class="img-fluid">
            </div>
            <div class="modal-footer justify-content-center">
              <button type="button" class="btn btn-success" data-bs-dismiss="modal">
                <i class="fas fa-times me-2"></i>Close
              </button>
            </div>
          </div>
        </div>
      </div>`;
    $("body").append(modal);
    $("#imageModal").modal("show");
    $("#imageModal").on("hidden.bs.modal", function () {
      $(this).remove();
    });
  });

  // Handle details button click
  $(document).on("click", "#btn-details", function () {
    const predictionText = $("#prediction-text").text().toLowerCase();
    let diseasePage = DISEASE_PAGE_MAPPING.unknown;

    for (const [key, value] of Object.entries(DISEASE_PAGE_MAPPING)) {
      if (predictionText.includes(key.toLowerCase())) {
        diseasePage = value;
        break;
      }
    }

    if (
      predictionText.includes("healthy") ||
      predictionText.includes("normal")
    ) {
      diseasePage = DISEASE_PAGE_MAPPING.healthy;
    }

    window.location.href = `/new/${diseasePage}`;
  });

  // Handle report submission
  $("#btn-submit-report").click(function () {
    const formData = {
      observations: $("#reportForm textarea").val(),
      email: $("#reportForm input[type='email']").val(),
      image_path: $("#original-image").attr("src"),
      prediction: $("#prediction-text").text(),
      confidence: $("#confidence-percent").text().replace("%", ""),
      timestamp: new Date().toISOString(),
    };

    if (!formData.observations) {
      alert("Please describe your observations");
      return;
    }

    $(this)
      .prop("disabled", true)
      .html(
        '<span class="spinner-border spinner-border-sm" role="status"></span> Submitting...'
      );

    $.ajax({
      type: "POST",
      url: "/report_unknown",
      data: formData,
      success: function () {
        $("#reportModal").modal("hide");
        alert("Thank you! Your report has been submitted.");
        $("#btn-submit-report")
          .prop("disabled", false)
          .html('<i class="fas fa-paper-plane me-2"></i>Submit Report');
      },
      error: function () {
        alert("Error submitting report. Please try again.");
        $("#btn-submit-report")
          .prop("disabled", false)
          .html('<i class="fas fa-paper-plane me-2"></i>Submit Report');
      },
    });
  });

  // Handle clear button click
  $("#btn-clear").click(function () {
    // Reset file input
    $("#imageUpload").val("");

    // Reset preview
    $("#imagePreview").css("background-image", "none");
    $(".image-section").hide();

    // Reset results
    $("#result-container").hide();
    $("#original-image").attr("src", "");
    $("#gradcam-image").attr("src", "");

    // Reset layout
    resetImageLayout();

    // Hide alerts and buttons
    $("#invalid-image-alert").hide();
    $("#unknown-disease-alert").hide();
    $("#btn-report").hide();
    $("#btn-details").hide();
    $("#btn-clear").hide();

    // Enable predict button
    $("#btn-predict").prop("disabled", false);

    // Scroll to upload section
    $("html, body").animate(
      {
        scrollTop: $("label[for='imageUpload']").offset().top - 20,
      },
      500
    );
  });
});

// Smooth scrolling for all anchor links
document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
  anchor.addEventListener("click", function (e) {
    e.preventDefault();
    document.querySelector(this.getAttribute("href")).scrollIntoView({
      behavior: "smooth",
    });
  });
});
