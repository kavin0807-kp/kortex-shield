<%@ page contentType="text/html;charset=UTF-8" language="java" %>
    <!DOCTYPE html>
    <html lang="en">

    <head>
        <meta charset="UTF-8">
        <title>App2 - Product Review</title>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600&display=swap');

            body {
                font-family: 'Montserrat', sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                background: #fafafa;
                margin: 0;
            }

            .card {
                display: flex;
                width: 800px;
                background: #fff;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
                border-radius: 10px;
                overflow: hidden;
            }

            .product-image {
                flex-basis: 50%;
                background: url('https://i.imgur.com/8u4y2V0.jpeg') center center/cover;
            }

            .review-form {
                flex-basis: 50%;
                padding: 40px;
                text-align: center;
            }

            h2 {
                margin-top: 0;
            }

            textarea {
                width: 100%;
                height: 100px;
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 5px;
                margin-bottom: 20px;
                resize: vertical;
                box-sizing: border-box;
            }

            .rating {
                margin-bottom: 20px;
            }

            .rating .star {
                font-size: 28px;
                color: #ddd;
                cursor: pointer;
                transition: color 0.2s;
            }

            .rating:hover .star {
                color: #f1c40f;
            }

            .rating .star:hover~.star {
                color: #ddd;
            }

            .submit-btn {
                background-color: #e74c3c;
                color: white;
                padding: 15px;
                border: none;
                border-radius: 5px;
                width: 100%;
                font-size: 16px;
                cursor: pointer;
            }

            .thank-you {
                color: #27ae60;
                font-weight: 600;
                display: none;
            }
        </style>
    </head>

    <body>
        <div class="card">
            <div class="product-image"></div>
            <div class="review-form">
                <h2>Review This Product</h2>
                <form id="reviewForm" action="/?app=app2" method="POST">
                    <div class="rating">
                        <span class="star" data-value="1">★</span><span class="star" data-value="2">★</span><span
                            class="star" data-value="3">★</span><span class="star" data-value="4">★</span><span
                            class="star" data-value="5">★</span>
                    </div>
                    <input type="hidden" name="rating" id="ratingValue" value="0">
                    <textarea name="review_text" placeholder="Share your thoughts..."></textarea>
                    <button type="submit" class="submit-btn">Submit Review</button>
                </form>
                <p class="thank-you" id="thankYouMessage">Thank you for your review!</p>
            </div>
        </div>
        <script>
            const stars = document.querySelectorAll('.star');
            const ratingValue = document.getElementById('ratingValue');
            stars.forEach(star => star.addEventListener('click', () => {
                const value = star.getAttribute('data-value');
                ratingValue.value = value;
                stars.forEach(s => s.style.color = s.getAttribute('data-value') <= value ? '#f1c40f' : '#ddd');
            }));
            document.getElementById('reviewForm').addEventListener('submit', function (e) {
                e.preventDefault();
                document.getElementById('thankYouMessage').style.display = 'block';
                this.style.display = 'none';
            });
        </script>
    </body>

    </html>