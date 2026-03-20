"""
Skill → Learning Resource Mapping
==================================
Each skill maps to a list of dicts with:
  - title  : human-readable course/resource name
  - url    : direct link
  - type   : "free" | "paid" | "freemium"
  - platform: source platform
"""

SKILL_RESOURCES: dict[str, list[dict]] = {

    # ─────────────────────────────────────────
    # LANGUAGES
    # ─────────────────────────────────────────
    "Python": [
        {"title": "Python for Everybody – University of Michigan", "url": "https://www.coursera.org/specializations/python", "type": "freemium", "platform": "Coursera"},
        {"title": "The Python Tutorial – Official Docs", "url": "https://docs.python.org/3/tutorial/", "type": "free", "platform": "python.org"},
        {"title": "freeCodeCamp – Python Full Course (6hrs)", "url": "https://www.youtube.com/watch?v=rfscVS0vtbw", "type": "free", "platform": "YouTube"},
        {"title": "Automate the Boring Stuff with Python", "url": "https://automatetheboringstuff.com/", "type": "free", "platform": "Book/Web"},
    ],
    "SQL": [
        {"title": "SQLZoo – Interactive SQL Tutorial", "url": "https://sqlzoo.net/", "type": "free", "platform": "SQLZoo"},
        {"title": "Mode SQL Tutorial", "url": "https://mode.com/sql-tutorial/", "type": "free", "platform": "Mode"},
        {"title": "freeCodeCamp – SQL Full Course", "url": "https://www.youtube.com/watch?v=HXV3zeQKqGY", "type": "free", "platform": "YouTube"},
        {"title": "The Complete SQL Bootcamp – Udemy", "url": "https://www.udemy.com/course/the-complete-sql-bootcamp/", "type": "paid", "platform": "Udemy"},
    ],
    "JavaScript": [
        {"title": "The Odin Project – Foundations", "url": "https://www.theodinproject.com/paths/foundations", "type": "free", "platform": "The Odin Project"},
        {"title": "JavaScript.info – Modern JS Tutorial", "url": "https://javascript.info/", "type": "free", "platform": "javascript.info"},
        {"title": "freeCodeCamp – JS Algorithms & Data Structures", "url": "https://www.freecodecamp.org/learn/javascript-algorithms-and-data-structures/", "type": "free", "platform": "freeCodeCamp"},
        {"title": "The Complete JavaScript Course – Udemy", "url": "https://www.udemy.com/course/the-complete-javascript-course/", "type": "paid", "platform": "Udemy"},
    ],
    "TypeScript": [
        {"title": "TypeScript Official Handbook", "url": "https://www.typescriptlang.org/docs/handbook/intro.html", "type": "free", "platform": "typescriptlang.org"},
        {"title": "Understanding TypeScript – Udemy", "url": "https://www.udemy.com/course/understanding-typescript/", "type": "paid", "platform": "Udemy"},
        {"title": "TypeScript Tutorial for Beginners – Traversy Media", "url": "https://www.youtube.com/watch?v=BCg4U1FzODs", "type": "free", "platform": "YouTube"},
    ],
    "Java": [
        {"title": "Java Programming & Software Engineering Fundamentals – Duke", "url": "https://www.coursera.org/specializations/java-programming", "type": "freemium", "platform": "Coursera"},
        {"title": "Java Tutorial for Beginners – Programming with Mosh", "url": "https://www.youtube.com/watch?v=eIrMbAQSU34", "type": "free", "platform": "YouTube"},
        {"title": "Java Documentation – Oracle", "url": "https://docs.oracle.com/en/java/", "type": "free", "platform": "Oracle"},
    ],
    "C++": [
        {"title": "C++ Tutorial for Beginners – freeCodeCamp", "url": "https://www.youtube.com/watch?v=vLnPwxZdW4Y", "type": "free", "platform": "YouTube"},
        {"title": "learncpp.com – Comprehensive C++ Tutorial", "url": "https://www.learncpp.com/", "type": "free", "platform": "learncpp.com"},
        {"title": "C++ Nanodegree – Udacity", "url": "https://www.udacity.com/course/c-plus-plus-nanodegree--nd213", "type": "paid", "platform": "Udacity"},
    ],
    "C#": [
        {"title": "C# Documentation – Microsoft Learn", "url": "https://learn.microsoft.com/en-us/dotnet/csharp/", "type": "free", "platform": "Microsoft Learn"},
        {"title": "C# Fundamentals for Absolute Beginners", "url": "https://learn.microsoft.com/en-us/shows/csharp-fundamentals-for-absolute-beginners/", "type": "free", "platform": "Microsoft Learn"},
        {"title": "Complete C# Unity Developer – Udemy", "url": "https://www.udemy.com/course/unitycourse/", "type": "paid", "platform": "Udemy"},
    ],
    "C": [
        {"title": "C Programming Tutorial – freeCodeCamp", "url": "https://www.youtube.com/watch?v=KJgsSFOSQv0", "type": "free", "platform": "YouTube"},
        {"title": "The C Programming Language (K&R) – Book", "url": "https://www.amazon.com/Programming-Language-2nd-Brian-Kernighan/dp/0131103628", "type": "paid", "platform": "Book"},
    ],
    "Go": [
        {"title": "A Tour of Go – Official", "url": "https://go.dev/tour/welcome/1", "type": "free", "platform": "go.dev"},
        {"title": "Go by Example", "url": "https://gobyexample.com/", "type": "free", "platform": "gobyexample.com"},
        {"title": "Learn Go with Tests", "url": "https://quii.gitbook.io/learn-go-with-tests/", "type": "free", "platform": "GitBook"},
    ],
    "Rust": [
        {"title": "The Rust Programming Language – Official Book", "url": "https://doc.rust-lang.org/book/", "type": "free", "platform": "rust-lang.org"},
        {"title": "Rustlings – Small Rust Exercises", "url": "https://github.com/rust-lang/rustlings", "type": "free", "platform": "GitHub"},
        {"title": "Rust by Example", "url": "https://doc.rust-lang.org/rust-by-example/", "type": "free", "platform": "rust-lang.org"},
    ],
    "Scala": [
        {"title": "Functional Programming Principles in Scala – EPFL", "url": "https://www.coursera.org/learn/scala-functional-programming", "type": "freemium", "platform": "Coursera"},
        {"title": "Scala Documentation – Official", "url": "https://docs.scala-lang.org/", "type": "free", "platform": "scala-lang.org"},
    ],
    "PHP": [
        {"title": "PHP Manual – Official Docs", "url": "https://www.php.net/manual/en/", "type": "free", "platform": "php.net"},
        {"title": "PHP for Beginners – Laracasts", "url": "https://laracasts.com/series/php-for-beginners-2023-edition", "type": "freemium", "platform": "Laracasts"},
    ],
    "Ruby": [
        {"title": "The Odin Project – Ruby Path", "url": "https://www.theodinproject.com/paths/full-stack-ruby-on-rails", "type": "free", "platform": "The Odin Project"},
        {"title": "Ruby Documentation – Official", "url": "https://www.ruby-lang.org/en/documentation/", "type": "free", "platform": "ruby-lang.org"},
    ],
    "Swift": [
        {"title": "Swift Documentation – Apple Developer", "url": "https://developer.apple.com/swift/resources/", "type": "free", "platform": "Apple Developer"},
        {"title": "Hacking with Swift", "url": "https://www.hackingwithswift.com/", "type": "free", "platform": "hackingwithswift.com"},
        {"title": "iOS & Swift – The Complete iOS App Development Bootcamp", "url": "https://www.udemy.com/course/ios-13-app-development-bootcamp/", "type": "paid", "platform": "Udemy"},
    ],
    "Kotlin": [
        {"title": "Kotlin Documentation – JetBrains", "url": "https://kotlinlang.org/docs/home.html", "type": "free", "platform": "kotlinlang.org"},
        {"title": "Kotlin for Java Developers – JetBrains on Coursera", "url": "https://www.coursera.org/learn/kotlin-for-java-developers", "type": "freemium", "platform": "Coursera"},
    ],
    "R": [
        {"title": "R for Data Science – Free Book", "url": "https://r4ds.had.co.nz/", "type": "free", "platform": "Book/Web"},
        {"title": "Statistics with R – Duke on Coursera", "url": "https://www.coursera.org/specializations/statistics", "type": "freemium", "platform": "Coursera"},
    ],
    "MATLAB": [
        {"title": "MATLAB Onramp – MathWorks (Free)", "url": "https://matlabacademy.mathworks.com/details/matlab-onramp/gettingstarted", "type": "free", "platform": "MathWorks"},
        {"title": "MATLAB Programming Techniques – Coursera", "url": "https://www.coursera.org/learn/matlab", "type": "freemium", "platform": "Coursera"},
    ],
    "Bash": [
        {"title": "The Linux Command Line – Free Book", "url": "https://linuxcommand.org/tlcl.php", "type": "free", "platform": "Book/Web"},
        {"title": "Bash Scripting Tutorial – Ryan's Tutorials", "url": "https://ryanstutorials.net/bash-scripting-tutorial/", "type": "free", "platform": "ryanstutorials.net"},
    ],
    "Shell": [
        {"title": "Shell Scripting Tutorial", "url": "https://www.shellscript.sh/", "type": "free", "platform": "shellscript.sh"},
        {"title": "Linux Shell Scripting – freeCodeCamp", "url": "https://www.youtube.com/watch?v=e7BufAVwDiM", "type": "free", "platform": "YouTube"},
    ],
    "Perl": [
        {"title": "Learn Perl – Official Tutorial", "url": "https://www.perl.org/learn.html", "type": "free", "platform": "perl.org"},
    ],
    "Groovy": [
        {"title": "Groovy Documentation – Apache", "url": "https://groovy-lang.org/documentation.html", "type": "free", "platform": "groovy-lang.org"},
    ],

    # ─────────────────────────────────────────
    # WEB & FRONTEND
    # ─────────────────────────────────────────
    "HTML": [
        {"title": "HTML – MDN Web Docs", "url": "https://developer.mozilla.org/en-US/docs/Learn/HTML", "type": "free", "platform": "MDN"},
        {"title": "Responsive Web Design – freeCodeCamp", "url": "https://www.freecodecamp.org/learn/2022/responsive-web-design/", "type": "free", "platform": "freeCodeCamp"},
    ],
    "CSS": [
        {"title": "CSS – MDN Web Docs", "url": "https://developer.mozilla.org/en-US/docs/Learn/CSS", "type": "free", "platform": "MDN"},
        {"title": "CSS Tricks – Complete Guide", "url": "https://css-tricks.com/guides/", "type": "free", "platform": "CSS-Tricks"},
    ],
    "HTML5": [
        {"title": "HTML5 – MDN Reference", "url": "https://developer.mozilla.org/en-US/docs/Web/Guide/HTML/HTML5", "type": "free", "platform": "MDN"},
    ],
    "CSS3": [
        {"title": "CSS3 Tutorial – W3Schools", "url": "https://www.w3schools.com/css/", "type": "free", "platform": "W3Schools"},
    ],
    "React": [
        {"title": "React Official Docs (New)", "url": "https://react.dev/learn", "type": "free", "platform": "react.dev"},
        {"title": "Full Stack Open – React Section", "url": "https://fullstackopen.com/en/", "type": "free", "platform": "University of Helsinki"},
        {"title": "React – The Complete Guide – Udemy", "url": "https://www.udemy.com/course/react-the-complete-guide-incl-redux/", "type": "paid", "platform": "Udemy"},
    ],
    "Vue": [
        {"title": "Vue.js Official Docs", "url": "https://vuejs.org/guide/introduction.html", "type": "free", "platform": "vuejs.org"},
        {"title": "Vue – The Complete Guide – Udemy", "url": "https://www.udemy.com/course/vuejs-2-the-complete-guide/", "type": "paid", "platform": "Udemy"},
    ],
    "Angular": [
        {"title": "Angular Official Tutorial", "url": "https://angular.dev/tutorials", "type": "free", "platform": "angular.dev"},
        {"title": "Angular – The Complete Guide – Udemy", "url": "https://www.udemy.com/course/the-complete-guide-to-angular-2/", "type": "paid", "platform": "Udemy"},
    ],
    "Next.js": [
        {"title": "Next.js Official Learn Course", "url": "https://nextjs.org/learn", "type": "free", "platform": "nextjs.org"},
        {"title": "Next.js & React – Udemy", "url": "https://www.udemy.com/course/nextjs-react-the-complete-guide/", "type": "paid", "platform": "Udemy"},
    ],
    "Nuxt.js": [
        {"title": "Nuxt.js Official Docs", "url": "https://nuxt.com/docs/getting-started/introduction", "type": "free", "platform": "nuxt.com"},
    ],
    "Node.js": [
        {"title": "Node.js Official Docs", "url": "https://nodejs.org/en/learn/getting-started/introduction-to-nodejs", "type": "free", "platform": "nodejs.org"},
        {"title": "Node.js, Express, MongoDB Bootcamp – Udemy", "url": "https://www.udemy.com/course/nodejs-express-mongodb-bootcamp/", "type": "paid", "platform": "Udemy"},
    ],
    "Express": [
        {"title": "Express.js Official Guide", "url": "https://expressjs.com/en/guide/routing.html", "type": "free", "platform": "expressjs.com"},
        {"title": "freeCodeCamp – Node & Express Tutorial", "url": "https://www.youtube.com/watch?v=Oe421EPjeBE", "type": "free", "platform": "YouTube"},
    ],
    "jQuery": [
        {"title": "jQuery Learning Center", "url": "https://learn.jquery.com/", "type": "free", "platform": "jquery.com"},
    ],
    "Bootstrap": [
        {"title": "Bootstrap Official Docs", "url": "https://getbootstrap.com/docs/5.3/getting-started/introduction/", "type": "free", "platform": "getbootstrap.com"},
    ],
    "Tailwind": [
        {"title": "Tailwind CSS Official Docs", "url": "https://tailwindcss.com/docs/installation", "type": "free", "platform": "tailwindcss.com"},
        {"title": "Tailwind CSS Tutorial – Net Ninja", "url": "https://www.youtube.com/watch?v=bxmDnn7lrnk&list=PL4cUxeGkcC9gpXORlEHjc5bgnIi5HEGhw", "type": "free", "platform": "YouTube"},
    ],
    "Sass": [
        {"title": "Sass Official Docs", "url": "https://sass-lang.com/guide/", "type": "free", "platform": "sass-lang.com"},
    ],
    "SCSS": [
        {"title": "SCSS Tutorial – W3Schools", "url": "https://www.w3schools.com/sass/", "type": "free", "platform": "W3Schools"},
    ],
    "Redux": [
        {"title": "Redux Official Tutorial", "url": "https://redux.js.org/tutorials/essentials/part-1-overview-concepts", "type": "free", "platform": "redux.js.org"},
    ],
    "GraphQL": [
        {"title": "GraphQL Official Learn", "url": "https://graphql.org/learn/", "type": "free", "platform": "graphql.org"},
        {"title": "Full Stack GraphQL – Apollo Odyssey", "url": "https://www.apollographql.com/tutorials/", "type": "free", "platform": "Apollo"},
    ],
    "REST": [
        {"title": "REST API Design – Best Practices (freeCodeCamp)", "url": "https://www.freecodecamp.org/news/rest-api-design-best-practices-build-a-rest-api/", "type": "free", "platform": "freeCodeCamp"},
    ],
    "REST APIs": [
        {"title": "REST API Tutorial", "url": "https://restfulapi.net/", "type": "free", "platform": "restfulapi.net"},
    ],
    "gRPC": [
        {"title": "gRPC Official Documentation", "url": "https://grpc.io/docs/", "type": "free", "platform": "grpc.io"},
    ],
    "WebSockets": [
        {"title": "WebSockets – MDN Guide", "url": "https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API", "type": "free", "platform": "MDN"},
    ],
    "AJAX": [
        {"title": "AJAX Introduction – W3Schools", "url": "https://www.w3schools.com/xml/ajax_intro.asp", "type": "free", "platform": "W3Schools"},
    ],

    # ─────────────────────────────────────────
    # BACKEND & AUTH
    # ─────────────────────────────────────────
    "FastAPI": [
        {"title": "FastAPI Official Tutorial", "url": "https://fastapi.tiangolo.com/tutorial/", "type": "free", "platform": "fastapi.tiangolo.com"},
        {"title": "FastAPI Full Course – freeCodeCamp", "url": "https://www.youtube.com/watch?v=0sOvCWFmrtA", "type": "free", "platform": "YouTube"},
    ],
    "Flask": [
        {"title": "Flask Official Tutorial", "url": "https://flask.palletsprojects.com/en/3.0.x/tutorial/", "type": "free", "platform": "flask.palletsprojects.com"},
        {"title": "Flask Web Development – Corey Schafer", "url": "https://www.youtube.com/watch?v=MwZwr5Tvyxo&list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH", "type": "free", "platform": "YouTube"},
    ],
    "Django": [
        {"title": "Django Official Tutorial", "url": "https://docs.djangoproject.com/en/5.0/intro/tutorial01/", "type": "free", "platform": "djangoproject.com"},
        {"title": "Django for Everybody – Coursera", "url": "https://www.coursera.org/specializations/django", "type": "freemium", "platform": "Coursera"},
    ],
    "Spring Boot": [
        {"title": "Spring Boot Official Guides", "url": "https://spring.io/guides", "type": "free", "platform": "spring.io"},
        {"title": "Spring Boot Tutorial – Amigoscode", "url": "https://www.youtube.com/watch?v=9SGDpanrc8U", "type": "free", "platform": "YouTube"},
    ],
    "Laravel": [
        {"title": "Laravel Official Documentation", "url": "https://laravel.com/docs", "type": "free", "platform": "laravel.com"},
        {"title": "Laravel 10 From Scratch – Laracasts", "url": "https://laracasts.com/series/30-days-to-learn-laravel-11", "type": "freemium", "platform": "Laracasts"},
    ],
    "Rails": [
        {"title": "Ruby on Rails Official Guides", "url": "https://guides.rubyonrails.org/", "type": "free", "platform": "rubyonrails.org"},
    ],
    "ASP.NET": [
        {"title": "ASP.NET Core Documentation – Microsoft Learn", "url": "https://learn.microsoft.com/en-us/aspnet/core/", "type": "free", "platform": "Microsoft Learn"},
    ],
    "JWT": [
        {"title": "JWT.io Introduction", "url": "https://jwt.io/introduction", "type": "free", "platform": "jwt.io"},
    ],
    "OAuth": [
        {"title": "OAuth 2.0 – Aaron Parecki", "url": "https://www.oauth.com/", "type": "free", "platform": "oauth.com"},
    ],
    "OAuth2": [
        {"title": "OAuth 2.0 Simplified – Book", "url": "https://www.oauth.com/", "type": "free", "platform": "oauth.com"},
    ],
    "OpenID": [
        {"title": "OpenID Connect Documentation", "url": "https://openid.net/developers/how-connect-works/", "type": "free", "platform": "openid.net"},
    ],
    "SAML": [
        {"title": "SAML Explained – Okta", "url": "https://developer.okta.com/docs/concepts/saml/", "type": "free", "platform": "Okta"},
    ],
    "Auth0": [
        {"title": "Auth0 Official Docs", "url": "https://auth0.com/docs", "type": "free", "platform": "auth0.com"},
    ],
    "Passport.js": [
        {"title": "Passport.js Official Docs", "url": "https://www.passportjs.org/docs/", "type": "free", "platform": "passportjs.org"},
    ],
    "Keycloak": [
        {"title": "Keycloak Official Documentation", "url": "https://www.keycloak.org/documentation", "type": "free", "platform": "keycloak.org"},
    ],
    "Microservices": [
        {"title": "Microservices – Martin Fowler", "url": "https://martinfowler.com/articles/microservices.html", "type": "free", "platform": "martinfowler.com"},
        {"title": "Microservices with Node.js & React – Udemy", "url": "https://www.udemy.com/course/microservices-with-node-js-and-react/", "type": "paid", "platform": "Udemy"},
    ],
    "Serverless": [
        {"title": "Serverless Framework Docs", "url": "https://www.serverless.com/framework/docs", "type": "free", "platform": "serverless.com"},
        {"title": "AWS Serverless on Coursera", "url": "https://www.coursera.org/learn/building-modern-java-applications-on-aws", "type": "freemium", "platform": "Coursera"},
    ],
    "API Gateway": [
        {"title": "AWS API Gateway Documentation", "url": "https://docs.aws.amazon.com/apigateway/latest/developerguide/welcome.html", "type": "free", "platform": "AWS Docs"},
    ],

    # ─────────────────────────────────────────
    # ML / AI
    # ─────────────────────────────────────────
    "PyTorch": [
        {"title": "PyTorch Official Tutorials", "url": "https://pytorch.org/tutorials/", "type": "free", "platform": "pytorch.org"},
        {"title": "Deep Learning with PyTorch – fast.ai", "url": "https://www.fast.ai/", "type": "free", "platform": "fast.ai"},
        {"title": "PyTorch for Deep Learning – Udemy", "url": "https://www.udemy.com/course/pytorch-for-deep-learning-and-computer-vision/", "type": "paid", "platform": "Udemy"},
    ],
    "TensorFlow": [
        {"title": "TensorFlow Official Tutorials", "url": "https://www.tensorflow.org/tutorials", "type": "free", "platform": "tensorflow.org"},
        {"title": "DeepLearning.AI TensorFlow Developer – Coursera", "url": "https://www.coursera.org/professional-certificates/tensorflow-in-practice", "type": "freemium", "platform": "Coursera"},
    ],
    "Keras": [
        {"title": "Keras Official Documentation", "url": "https://keras.io/getting_started/", "type": "free", "platform": "keras.io"},
    ],
    "Scikit-learn": [
        {"title": "Scikit-learn Official User Guide", "url": "https://scikit-learn.org/stable/user_guide.html", "type": "free", "platform": "scikit-learn.org"},
        {"title": "ML with Python & Scikit-learn – freeCodeCamp", "url": "https://www.youtube.com/watch?v=hDKCxebp88A", "type": "free", "platform": "YouTube"},
    ],
    "XGBoost": [
        {"title": "XGBoost Official Docs & Tutorials", "url": "https://xgboost.readthedocs.io/en/stable/tutorials/", "type": "free", "platform": "xgboost.readthedocs.io"},
    ],
    "LightGBM": [
        {"title": "LightGBM Official Documentation", "url": "https://lightgbm.readthedocs.io/en/latest/", "type": "free", "platform": "lightgbm.readthedocs.io"},
    ],
    "CatBoost": [
        {"title": "CatBoost Official Tutorials", "url": "https://catboost.ai/docs/concepts/tutorials.html", "type": "free", "platform": "catboost.ai"},
    ],
    "Hugging Face": [
        {"title": "Hugging Face NLP Course", "url": "https://huggingface.co/learn/nlp-course/chapter1/1", "type": "free", "platform": "Hugging Face"},
        {"title": "Hugging Face Documentation", "url": "https://huggingface.co/docs", "type": "free", "platform": "Hugging Face"},
    ],
    "BERT": [
        {"title": "BERT Explained – Illustrated Transformer", "url": "https://jalammar.github.io/illustrated-bert/", "type": "free", "platform": "jalammar.github.io"},
        {"title": "Hugging Face BERT Fine-tuning Tutorial", "url": "https://huggingface.co/docs/transformers/training", "type": "free", "platform": "Hugging Face"},
    ],
    "GPT": [
        {"title": "GPT Fine-tuning – OpenAI Docs", "url": "https://platform.openai.com/docs/guides/fine-tuning", "type": "free", "platform": "OpenAI"},
        {"title": "Andrej Karpathy – Let's Build GPT (YouTube)", "url": "https://www.youtube.com/watch?v=kCc8FmEb1nY", "type": "free", "platform": "YouTube"},
    ],
    "LLM": [
        {"title": "Large Language Models – DeepLearning.AI Short Course", "url": "https://www.deeplearning.ai/short-courses/", "type": "free", "platform": "DeepLearning.AI"},
        {"title": "LLM Bootcamp – Full Stack Deep Learning", "url": "https://fullstackdeeplearning.com/llm-bootcamp/", "type": "free", "platform": "FSDL"},
    ],
    "NLP": [
        {"title": "Stanford NLP with Deep Learning – CS224N", "url": "https://web.stanford.edu/class/cs224n/", "type": "free", "platform": "Stanford"},
        {"title": "Hugging Face NLP Course", "url": "https://huggingface.co/learn/nlp-course/chapter1/1", "type": "free", "platform": "Hugging Face"},
    ],
    "Computer Vision": [
        {"title": "Stanford CS231n – Convolutional Neural Networks", "url": "http://cs231n.stanford.edu/", "type": "free", "platform": "Stanford"},
        {"title": "Computer Vision with Python – freeCodeCamp", "url": "https://www.youtube.com/watch?v=oXlwWbU8l2o", "type": "free", "platform": "YouTube"},
    ],
    "OpenCV": [
        {"title": "OpenCV Official Documentation & Tutorials", "url": "https://docs.opencv.org/4.x/d9/df8/tutorial_root.html", "type": "free", "platform": "opencv.org"},
        {"title": "OpenCV Python Tutorial – freeCodeCamp", "url": "https://www.youtube.com/watch?v=oXlwWbU8l2o", "type": "free", "platform": "YouTube"},
    ],
    "Pandas": [
        {"title": "Pandas Official Getting Started", "url": "https://pandas.pydata.org/docs/getting_started/index.html", "type": "free", "platform": "pandas.pydata.org"},
        {"title": "Pandas Tutorial – Corey Schafer", "url": "https://www.youtube.com/watch?v=ZyhVh-qRZPA&list=PL-osiE80TeTsWmV9i9c58mdDCSskIFdDS", "type": "free", "platform": "YouTube"},
    ],
    "NumPy": [
        {"title": "NumPy Official Documentation", "url": "https://numpy.org/learn/", "type": "free", "platform": "numpy.org"},
        {"title": "NumPy Tutorial – freeCodeCamp", "url": "https://www.youtube.com/watch?v=QUT1VHiLmmI", "type": "free", "platform": "YouTube"},
    ],
    "Matplotlib": [
        {"title": "Matplotlib Official Tutorials", "url": "https://matplotlib.org/stable/tutorials/index.html", "type": "free", "platform": "matplotlib.org"},
    ],
    "Seaborn": [
        {"title": "Seaborn Official Tutorial", "url": "https://seaborn.pydata.org/tutorial.html", "type": "free", "platform": "seaborn.pydata.org"},
    ],
    "Plotly": [
        {"title": "Plotly Python Open Source Documentation", "url": "https://plotly.com/python/", "type": "free", "platform": "plotly.com"},
    ],
    "SciPy": [
        {"title": "SciPy Official Documentation", "url": "https://docs.scipy.org/doc/scipy/tutorial/index.html", "type": "free", "platform": "scipy.org"},
    ],
    "StatsModels": [
        {"title": "StatsModels Official Docs", "url": "https://www.statsmodels.org/stable/gettingstarted.html", "type": "free", "platform": "statsmodels.org"},
    ],

    # ─────────────────────────────────────────
    # DATA ENGINEERING
    # ─────────────────────────────────────────
    "Kafka": [
        {"title": "Apache Kafka Official Documentation", "url": "https://kafka.apache.org/documentation/", "type": "free", "platform": "kafka.apache.org"},
        {"title": "Apache Kafka Series – Udemy (Stephane Maarek)", "url": "https://www.udemy.com/course/apache-kafka/", "type": "paid", "platform": "Udemy"},
    ],
    "Spark": [
        {"title": "Apache Spark Official Documentation", "url": "https://spark.apache.org/docs/latest/", "type": "free", "platform": "spark.apache.org"},
        {"title": "Spark & Python for Big Data – Udemy", "url": "https://www.udemy.com/course/spark-and-python-for-big-data-with-pyspark/", "type": "paid", "platform": "Udemy"},
    ],
    "PySpark": [
        {"title": "PySpark Documentation", "url": "https://spark.apache.org/docs/latest/api/python/getting_started/index.html", "type": "free", "platform": "spark.apache.org"},
        {"title": "PySpark Tutorial – freeCodeCamp", "url": "https://www.youtube.com/watch?v=_C8kWso4ne4", "type": "free", "platform": "YouTube"},
    ],
    "Dask": [
        {"title": "Dask Official Documentation", "url": "https://docs.dask.org/en/stable/", "type": "free", "platform": "dask.org"},
    ],
    "Flink": [
        {"title": "Apache Flink Official Documentation", "url": "https://nightlies.apache.org/flink/flink-docs-stable/", "type": "free", "platform": "flink.apache.org"},
    ],
    "Airflow": [
        {"title": "Apache Airflow Official Documentation", "url": "https://airflow.apache.org/docs/", "type": "free", "platform": "airflow.apache.org"},
        {"title": "The Complete Hands-On Apache Airflow – Udemy", "url": "https://www.udemy.com/course/the-complete-hands-on-course-to-master-apache-airflow/", "type": "paid", "platform": "Udemy"},
    ],
    "Luigi": [
        {"title": "Luigi Official Documentation", "url": "https://luigi.readthedocs.io/en/stable/", "type": "free", "platform": "readthedocs.io"},
    ],
    "Prefect": [
        {"title": "Prefect Official Documentation", "url": "https://docs.prefect.io/latest/", "type": "free", "platform": "prefect.io"},
    ],
    "dbt": [
        {"title": "dbt Learn – Official Free Courses", "url": "https://learn.getdbt.com/", "type": "free", "platform": "getdbt.com"},
        {"title": "dbt Official Documentation", "url": "https://docs.getdbt.com/", "type": "free", "platform": "getdbt.com"},
    ],
    "ETL": [
        {"title": "ETL Concepts – Informatica Tutorial", "url": "https://www.guru99.com/etl-extract-load-process.html", "type": "free", "platform": "guru99.com"},
    ],
    "ELT": [
        {"title": "ELT vs ETL Explained – dbt Blog", "url": "https://www.getdbt.com/blog/etl-vs-elt/", "type": "free", "platform": "getdbt.com"},
    ],
    "Data Pipeline": [
        {"title": "Data Engineering Zoomcamp – DataTalks.Club", "url": "https://github.com/DataTalksClub/data-engineering-zoomcamp", "type": "free", "platform": "GitHub"},
    ],
    "Hadoop": [
        {"title": "Hadoop Tutorial – Apache Official", "url": "https://hadoop.apache.org/docs/stable/", "type": "free", "platform": "hadoop.apache.org"},
    ],
    "Hive": [
        {"title": "Apache Hive Documentation", "url": "https://cwiki.apache.org/confluence/display/Hive/Home", "type": "free", "platform": "apache.org"},
    ],
    "Presto": [
        {"title": "Presto Official Documentation", "url": "https://prestodb.io/docs/current/", "type": "free", "platform": "prestodb.io"},
    ],
    "Trino": [
        {"title": "Trino Official Documentation", "url": "https://trino.io/docs/current/", "type": "free", "platform": "trino.io"},
    ],

    # ─────────────────────────────────────────
    # DATABASES
    # ─────────────────────────────────────────
    "PostgreSQL": [
        {"title": "PostgreSQL Official Tutorial", "url": "https://www.postgresql.org/docs/current/tutorial.html", "type": "free", "platform": "postgresql.org"},
        {"title": "PostgreSQL Tutorial – postgresqltutorial.com", "url": "https://www.postgresqltutorial.com/", "type": "free", "platform": "postgresqltutorial.com"},
    ],
    "MySQL": [
        {"title": "MySQL Official Documentation", "url": "https://dev.mysql.com/doc/", "type": "free", "platform": "mysql.com"},
        {"title": "MySQL Crash Course – freeCodeCamp", "url": "https://www.youtube.com/watch?v=7S_tz1z_5bA", "type": "free", "platform": "YouTube"},
    ],
    "SQLite": [
        {"title": "SQLite Official Documentation", "url": "https://www.sqlite.org/docs.html", "type": "free", "platform": "sqlite.org"},
    ],
    "Oracle": [
        {"title": "Oracle Database Documentation", "url": "https://docs.oracle.com/en/database/", "type": "free", "platform": "oracle.com"},
    ],
    "SQL Server": [
        {"title": "SQL Server Documentation – Microsoft", "url": "https://learn.microsoft.com/en-us/sql/sql-server/", "type": "free", "platform": "Microsoft Learn"},
    ],
    "MongoDB": [
        {"title": "MongoDB University – Free Courses", "url": "https://learn.mongodb.com/", "type": "free", "platform": "MongoDB University"},
        {"title": "MongoDB Official Documentation", "url": "https://www.mongodb.com/docs/", "type": "free", "platform": "mongodb.com"},
    ],
    "Redis": [
        {"title": "Redis Official Documentation", "url": "https://redis.io/docs/", "type": "free", "platform": "redis.io"},
        {"title": "Redis University – Free Courses", "url": "https://university.redis.com/", "type": "free", "platform": "Redis University"},
    ],
    "Cassandra": [
        {"title": "Apache Cassandra Documentation", "url": "https://cassandra.apache.org/doc/latest/", "type": "free", "platform": "cassandra.apache.org"},
        {"title": "DataStax Cassandra Fundamentals – Free", "url": "https://www.datastax.com/dev/cassandra", "type": "free", "platform": "DataStax"},
    ],
    "DynamoDB": [
        {"title": "DynamoDB Developer Guide – AWS", "url": "https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html", "type": "free", "platform": "AWS Docs"},
    ],
    "Elasticsearch": [
        {"title": "Elasticsearch Official Documentation", "url": "https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html", "type": "free", "platform": "elastic.co"},
    ],
    "Neo4j": [
        {"title": "Neo4j GraphAcademy – Free Courses", "url": "https://graphacademy.neo4j.com/", "type": "free", "platform": "Neo4j GraphAcademy"},
    ],
    "InfluxDB": [
        {"title": "InfluxDB Official Documentation", "url": "https://docs.influxdata.com/influxdb/", "type": "free", "platform": "influxdata.com"},
    ],
    "Firestore": [
        {"title": "Firebase Firestore Documentation", "url": "https://firebase.google.com/docs/firestore", "type": "free", "platform": "Firebase"},
    ],
    "Snowflake": [
        {"title": "Snowflake Official Documentation", "url": "https://docs.snowflake.com/en/", "type": "free", "platform": "snowflake.com"},
        {"title": "Snowflake Hands-On Essentials (Free)", "url": "https://learn.snowflake.com/en/courses/uni-ess-dwhopt/", "type": "free", "platform": "Snowflake Learn"},
    ],
    "BigQuery": [
        {"title": "BigQuery Official Documentation", "url": "https://cloud.google.com/bigquery/docs", "type": "free", "platform": "Google Cloud"},
        {"title": "BigQuery for Data Analysts – Google Skill Boost", "url": "https://www.cloudskillsboost.google/course_templates/560", "type": "freemium", "platform": "Google Cloud Skills Boost"},
    ],
    "Redshift": [
        {"title": "Amazon Redshift Documentation", "url": "https://docs.aws.amazon.com/redshift/latest/dg/welcome.html", "type": "free", "platform": "AWS Docs"},
    ],
    "Databricks": [
        {"title": "Databricks Academy – Free Training", "url": "https://www.databricks.com/learn/training/home", "type": "freemium", "platform": "Databricks Academy"},
    ],
    "Delta Lake": [
        {"title": "Delta Lake Official Documentation", "url": "https://docs.delta.io/latest/index.html", "type": "free", "platform": "delta.io"},
    ],

    # ─────────────────────────────────────────
    # CLOUD & DEVOPS
    # ─────────────────────────────────────────
    "AWS": [
        {"title": "AWS Skill Builder – Free Courses", "url": "https://explore.skillbuilder.aws/learn", "type": "freemium", "platform": "AWS Skill Builder"},
        {"title": "AWS Certified Solutions Architect – Udemy (A. Cantrill)", "url": "https://www.udemy.com/course/aws-certified-solutions-architect-associate-saa-c03/", "type": "paid", "platform": "Udemy"},
    ],
    "GCP": [
        {"title": "Google Cloud Skills Boost", "url": "https://www.cloudskillsboost.google/", "type": "freemium", "platform": "Google Cloud"},
        {"title": "Google Cloud Digital Leader – Coursera", "url": "https://www.coursera.org/professional-certificates/google-cloud-digital-leader-training", "type": "freemium", "platform": "Coursera"},
    ],
    "Azure": [
        {"title": "Microsoft Azure Fundamentals – Microsoft Learn", "url": "https://learn.microsoft.com/en-us/training/paths/azure-fundamentals/", "type": "free", "platform": "Microsoft Learn"},
        {"title": "AZ-900 Azure Fundamentals – freeCodeCamp", "url": "https://www.youtube.com/watch?v=NKEFWyqJ5XA", "type": "free", "platform": "YouTube"},
    ],
    "EC2": [
        {"title": "Amazon EC2 Documentation", "url": "https://docs.aws.amazon.com/ec2/", "type": "free", "platform": "AWS Docs"},
    ],
    "S3": [
        {"title": "Amazon S3 Documentation", "url": "https://docs.aws.amazon.com/s3/", "type": "free", "platform": "AWS Docs"},
    ],
    "Lambda": [
        {"title": "AWS Lambda Documentation", "url": "https://docs.aws.amazon.com/lambda/latest/dg/welcome.html", "type": "free", "platform": "AWS Docs"},
    ],
    "RDS": [
        {"title": "Amazon RDS Documentation", "url": "https://docs.aws.amazon.com/rds/", "type": "free", "platform": "AWS Docs"},
    ],
    "ECS": [
        {"title": "Amazon ECS Documentation", "url": "https://docs.aws.amazon.com/ecs/", "type": "free", "platform": "AWS Docs"},
    ],
    "EKS": [
        {"title": "Amazon EKS Documentation", "url": "https://docs.aws.amazon.com/eks/latest/userguide/what-is-eks.html", "type": "free", "platform": "AWS Docs"},
    ],
    "CloudFormation": [
        {"title": "AWS CloudFormation Documentation", "url": "https://docs.aws.amazon.com/cloudformation/", "type": "free", "platform": "AWS Docs"},
    ],
    "Kubernetes": [
        {"title": "Kubernetes Official Documentation", "url": "https://kubernetes.io/docs/tutorials/", "type": "free", "platform": "kubernetes.io"},
        {"title": "Kubernetes for Absolute Beginners – KodeKloud (Udemy)", "url": "https://www.udemy.com/course/learn-kubernetes/", "type": "paid", "platform": "Udemy"},
    ],
    "Docker": [
        {"title": "Docker Official Get Started Tutorial", "url": "https://docs.docker.com/get-started/", "type": "free", "platform": "docker.com"},
        {"title": "Docker & Kubernetes – Udemy (S. Grider)", "url": "https://www.udemy.com/course/docker-and-kubernetes-the-complete-guide/", "type": "paid", "platform": "Udemy"},
    ],
    "Terraform": [
        {"title": "Terraform Official Tutorials – HashiCorp", "url": "https://developer.hashicorp.com/terraform/tutorials", "type": "free", "platform": "HashiCorp"},
        {"title": "Terraform on AWS/GCP/Azure – Udemy", "url": "https://www.udemy.com/course/terraform-beginner-to-advanced/", "type": "paid", "platform": "Udemy"},
    ],
    "Ansible": [
        {"title": "Ansible Official Documentation", "url": "https://docs.ansible.com/", "type": "free", "platform": "ansible.com"},
        {"title": "Ansible for DevOps – Jeff Geerling (Free Book)", "url": "https://www.ansiblefordevops.com/", "type": "free", "platform": "Book/Web"},
    ],
    "Helm": [
        {"title": "Helm Official Documentation", "url": "https://helm.sh/docs/", "type": "free", "platform": "helm.sh"},
    ],
    "Jenkins": [
        {"title": "Jenkins Official Documentation", "url": "https://www.jenkins.io/doc/tutorials/", "type": "free", "platform": "jenkins.io"},
    ],
    "GitHub Actions": [
        {"title": "GitHub Actions Official Docs", "url": "https://docs.github.com/en/actions", "type": "free", "platform": "GitHub Docs"},
        {"title": "GitHub Actions Tutorial – TechWorld with Nana", "url": "https://www.youtube.com/watch?v=R8_veQiYBjI", "type": "free", "platform": "YouTube"},
    ],
    "CircleCI": [
        {"title": "CircleCI Official Documentation", "url": "https://circleci.com/docs/", "type": "free", "platform": "circleci.com"},
    ],
    "ArgoCD": [
        {"title": "Argo CD Official Documentation", "url": "https://argo-cd.readthedocs.io/en/stable/", "type": "free", "platform": "readthedocs.io"},
    ],
    "CI/CD": [
        {"title": "CI/CD Explained – GitLab", "url": "https://about.gitlab.com/topics/ci-cd/", "type": "free", "platform": "GitLab"},
        {"title": "DevOps & CI/CD – freeCodeCamp", "url": "https://www.youtube.com/watch?v=j5Zsa_eOXeY", "type": "free", "platform": "YouTube"},
    ],
    "DevOps": [
        {"title": "DevOps Roadmap – roadmap.sh", "url": "https://roadmap.sh/devops", "type": "free", "platform": "roadmap.sh"},
        {"title": "DevOps Bootcamp – TechWorld with Nana", "url": "https://www.youtube.com/watch?v=0yWAtQ6wYNM", "type": "free", "platform": "YouTube"},
    ],
    "SRE": [
        {"title": "Google SRE Book – Free Online", "url": "https://sre.google/sre-book/table-of-contents/", "type": "free", "platform": "Google"},
    ],
    "Linux": [
        {"title": "Linux Journey – Interactive Tutorial", "url": "https://linuxjourney.com/", "type": "free", "platform": "linuxjourney.com"},
        {"title": "The Linux Command Line – Free Book", "url": "https://linuxcommand.org/tlcl.php", "type": "free", "platform": "Book/Web"},
    ],
    "Nginx": [
        {"title": "Nginx Official Documentation", "url": "https://nginx.org/en/docs/", "type": "free", "platform": "nginx.org"},
        {"title": "Nginx Tutorial for Beginners – TechWorld with Nana", "url": "https://www.youtube.com/watch?v=7VAI73roXaY", "type": "free", "platform": "YouTube"},
    ],
    "Apache": [
        {"title": "Apache HTTP Server Documentation", "url": "https://httpd.apache.org/docs/", "type": "free", "platform": "apache.org"},
    ],

    # ─────────────────────────────────────────
    # MLOPS
    # ─────────────────────────────────────────
    "MLflow": [
        {"title": "MLflow Official Documentation", "url": "https://mlflow.org/docs/latest/index.html", "type": "free", "platform": "mlflow.org"},
    ],
    "Kubeflow": [
        {"title": "Kubeflow Official Documentation", "url": "https://www.kubeflow.org/docs/", "type": "free", "platform": "kubeflow.org"},
    ],
    "BentoML": [
        {"title": "BentoML Official Documentation", "url": "https://docs.bentoml.com/", "type": "free", "platform": "bentoml.com"},
    ],
    "Seldon": [
        {"title": "Seldon Core Documentation", "url": "https://docs.seldon.io/projects/seldon-core/en/latest/", "type": "free", "platform": "seldon.io"},
    ],
    "Feast": [
        {"title": "Feast Official Documentation", "url": "https://docs.feast.dev/", "type": "free", "platform": "feast.dev"},
    ],
    "Tecton": [
        {"title": "Tecton Official Documentation", "url": "https://docs.tecton.ai/", "type": "free", "platform": "tecton.ai"},
    ],
    "DVC": [
        {"title": "DVC Official Documentation", "url": "https://dvc.org/doc", "type": "free", "platform": "dvc.org"},
    ],
    "Weights & Biases": [
        {"title": "Weights & Biases Official Courses", "url": "https://www.wandb.courses/", "type": "free", "platform": "wandb.ai"},
        {"title": "W&B Official Documentation", "url": "https://docs.wandb.ai/", "type": "free", "platform": "wandb.ai"},
    ],
    "Pinecone": [
        {"title": "Pinecone Official Documentation", "url": "https://docs.pinecone.io/", "type": "free", "platform": "pinecone.io"},
        {"title": "Pinecone Learning Center", "url": "https://www.pinecone.io/learn/", "type": "free", "platform": "pinecone.io"},
    ],
    "Weaviate": [
        {"title": "Weaviate Official Documentation", "url": "https://weaviate.io/developers/weaviate", "type": "free", "platform": "weaviate.io"},
    ],
    "Chroma": [
        {"title": "Chroma Official Documentation", "url": "https://docs.trychroma.com/", "type": "free", "platform": "trychroma.com"},
    ],
    "FAISS": [
        {"title": "FAISS Official Documentation – Meta", "url": "https://faiss.ai/", "type": "free", "platform": "faiss.ai"},
        {"title": "FAISS Getting Started – GitHub Wiki", "url": "https://github.com/facebookresearch/faiss/wiki/Getting-started", "type": "free", "platform": "GitHub"},
    ],
    "LangChain": [
        {"title": "LangChain Official Documentation", "url": "https://python.langchain.com/docs/introduction/", "type": "free", "platform": "langchain.com"},
        {"title": "LangChain Course – DeepLearning.AI", "url": "https://www.deeplearning.ai/short-courses/langchain-for-llm-application-development/", "type": "free", "platform": "DeepLearning.AI"},
    ],
    "LlamaIndex": [
        {"title": "LlamaIndex Official Documentation", "url": "https://docs.llamaindex.ai/en/stable/", "type": "free", "platform": "llamaindex.ai"},
        {"title": "LlamaIndex Course – DeepLearning.AI", "url": "https://www.deeplearning.ai/short-courses/building-agentic-rag-with-llamaindex/", "type": "free", "platform": "DeepLearning.AI"},
    ],

    # ─────────────────────────────────────────
    # TOOLS & PRACTICES
    # ─────────────────────────────────────────
    "Git": [
        {"title": "Pro Git Book – Free Online", "url": "https://git-scm.com/book/en/v2", "type": "free", "platform": "git-scm.com"},
        {"title": "Git & GitHub Crash Course – freeCodeCamp", "url": "https://www.youtube.com/watch?v=RGOj5yH7evk", "type": "free", "platform": "YouTube"},
    ],
    "GitHub": [
        {"title": "GitHub Skills – Official Interactive Courses", "url": "https://skills.github.com/", "type": "free", "platform": "GitHub"},
        {"title": "GitHub Documentation", "url": "https://docs.github.com/en", "type": "free", "platform": "GitHub Docs"},
    ],
    "GitLab": [
        {"title": "GitLab Official Documentation", "url": "https://docs.gitlab.com/", "type": "free", "platform": "GitLab"},
    ],
    "Bitbucket": [
        {"title": "Bitbucket Official Documentation", "url": "https://support.atlassian.com/bitbucket-cloud/", "type": "free", "platform": "Atlassian"},
    ],
    "Jira": [
        {"title": "Jira Software Tutorials – Atlassian University", "url": "https://university.atlassian.com/student/catalog/list?category_ids=701548-jira", "type": "free", "platform": "Atlassian University"},
    ],
    "Confluence": [
        {"title": "Confluence Tutorials – Atlassian University", "url": "https://university.atlassian.com/student/catalog/list?category_ids=701549-confluence", "type": "free", "platform": "Atlassian University"},
    ],
    "Notion": [
        {"title": "Notion Official Guides & Tutorials", "url": "https://www.notion.com/guides", "type": "free", "platform": "notion.com"},
    ],
    "Tableau": [
        {"title": "Tableau e-Learning – Free for Students", "url": "https://www.tableau.com/academic/students", "type": "freemium", "platform": "Tableau"},
        {"title": "Tableau Public Gallery & How-To", "url": "https://www.tableau.com/learn/training", "type": "free", "platform": "Tableau"},
    ],
    "Power BI": [
        {"title": "Power BI Guided Learning – Microsoft Learn", "url": "https://learn.microsoft.com/en-us/power-bi/guided-learning/", "type": "free", "platform": "Microsoft Learn"},
        {"title": "Microsoft Power BI Desktop – freeCodeCamp", "url": "https://www.youtube.com/watch?v=TmhQCQr_0ls", "type": "free", "platform": "YouTube"},
    ],
    "Looker": [
        {"title": "Looker Official Documentation", "url": "https://cloud.google.com/looker/docs", "type": "free", "platform": "Google Cloud"},
    ],
    "Metabase": [
        {"title": "Metabase Official Documentation", "url": "https://www.metabase.com/docs/latest/", "type": "free", "platform": "metabase.com"},
    ],
    "Grafana": [
        {"title": "Grafana Official Documentation & Tutorials", "url": "https://grafana.com/tutorials/", "type": "free", "platform": "grafana.com"},
    ],
    "Prometheus": [
        {"title": "Prometheus Official Documentation", "url": "https://prometheus.io/docs/introduction/overview/", "type": "free", "platform": "prometheus.io"},
    ],
    "Datadog": [
        {"title": "Datadog Learning Center", "url": "https://learn.datadoghq.com/", "type": "freemium", "platform": "Datadog"},
    ],
    "Postman": [
        {"title": "Postman Learning Center", "url": "https://learning.postman.com/", "type": "free", "platform": "Postman"},
    ],
    "Swagger": [
        {"title": "Swagger Official Documentation", "url": "https://swagger.io/docs/specification/about/", "type": "free", "platform": "swagger.io"},
    ],
    "OpenAPI": [
        {"title": "OpenAPI Specification – Official Docs", "url": "https://spec.openapis.org/oas/latest.html", "type": "free", "platform": "openapis.org"},
    ],
    "Jupyter": [
        {"title": "Jupyter Official Documentation", "url": "https://docs.jupyter.org/en/latest/", "type": "free", "platform": "jupyter.org"},
        {"title": "Jupyter Notebook Tutorial – DataQuest", "url": "https://www.dataquest.io/blog/jupyter-notebook-tutorial/", "type": "free", "platform": "DataQuest"},
    ],
    "VS Code": [
        {"title": "VS Code Official Documentation", "url": "https://code.visualstudio.com/docs", "type": "free", "platform": "code.visualstudio.com"},
    ],
    "PyCharm": [
        {"title": "PyCharm Official Guide – JetBrains", "url": "https://www.jetbrains.com/help/pycharm/quick-start-guide.html", "type": "free", "platform": "JetBrains"},
    ],

    # ─────────────────────────────────────────
    # TESTING & SECURITY
    # ─────────────────────────────────────────
    "Pytest": [
        {"title": "Pytest Official Documentation", "url": "https://docs.pytest.org/en/stable/", "type": "free", "platform": "pytest.org"},
        {"title": "Python Testing with Pytest – Book (Sample)", "url": "https://pragprog.com/titles/bopytest2/python-testing-with-pytest-second-edition/", "type": "paid", "platform": "Pragmatic Bookshelf"},
    ],
    "Jest": [
        {"title": "Jest Official Documentation", "url": "https://jestjs.io/docs/getting-started", "type": "free", "platform": "jestjs.io"},
    ],
    "Selenium": [
        {"title": "Selenium Official Documentation", "url": "https://www.selenium.dev/documentation/", "type": "free", "platform": "selenium.dev"},
        {"title": "Selenium WebDriver with Python – freeCodeCamp", "url": "https://www.youtube.com/watch?v=j7VZsCCnptM", "type": "free", "platform": "YouTube"},
    ],
    "Cypress": [
        {"title": "Cypress Official Documentation", "url": "https://docs.cypress.io/guides/overview/why-cypress", "type": "free", "platform": "cypress.io"},
    ],
    "Playwright": [
        {"title": "Playwright Official Documentation", "url": "https://playwright.dev/docs/intro", "type": "free", "platform": "playwright.dev"},
    ],
    "JUnit": [
        {"title": "JUnit 5 Official User Guide", "url": "https://junit.org/junit5/docs/current/user-guide/", "type": "free", "platform": "junit.org"},
    ],
    "Mocha": [
        {"title": "Mocha Official Documentation", "url": "https://mochajs.org/", "type": "free", "platform": "mochajs.org"},
    ],
    "HTTPS": [
        {"title": "HTTPS Explained – Mozilla", "url": "https://developer.mozilla.org/en-US/docs/Web/HTTP/Overview", "type": "free", "platform": "MDN"},
    ],
    "SSL": [
        {"title": "SSL/TLS Explained – Cloudflare", "url": "https://www.cloudflare.com/learning/ssl/what-is-ssl/", "type": "free", "platform": "Cloudflare"},
    ],
    "TLS": [
        {"title": "TLS 1.3 – IETF Documentation", "url": "https://www.cloudflare.com/learning/ssl/transport-layer-security-tls/", "type": "free", "platform": "Cloudflare"},
    ],
    "OWASP": [
        {"title": "OWASP Top 10 – Official", "url": "https://owasp.org/www-project-top-ten/", "type": "free", "platform": "owasp.org"},
        {"title": "OWASP WebGoat – Hands-on Security Lab", "url": "https://owasp.org/www-project-webgoat/", "type": "free", "platform": "owasp.org"},
    ],
    "Penetration Testing": [
        {"title": "Ethical Hacking – TCM Security (YouTube)", "url": "https://www.youtube.com/watch?v=3Kq1MIfTWCE", "type": "free", "platform": "YouTube"},
        {"title": "TryHackMe – Hands-on Penetration Testing", "url": "https://tryhackme.com/", "type": "freemium", "platform": "TryHackMe"},
        {"title": "Penetration Testing Bootcamp – Udemy", "url": "https://www.udemy.com/course/complete-ethical-hacking-bootcamp-zero-to-mastery/", "type": "paid", "platform": "Udemy"},
    ],

    # ─────────────────────────────────────────
    # CONCEPTS
    # ─────────────────────────────────────────
    "Machine Learning": [
        {"title": "Machine Learning Specialization – Andrew Ng (Coursera)", "url": "https://www.coursera.org/specializations/machine-learning-introduction", "type": "freemium", "platform": "Coursera"},
        {"title": "Hands-On ML with Scikit-Learn & TensorFlow – O'Reilly", "url": "https://www.oreilly.com/library/view/hands-on-machine-learning/9781492032632/", "type": "paid", "platform": "O'Reilly"},
        {"title": "ML Crash Course – Google", "url": "https://developers.google.com/machine-learning/crash-course", "type": "free", "platform": "Google Developers"},
    ],
    "Deep Learning": [
        {"title": "Deep Learning Specialization – Andrew Ng (Coursera)", "url": "https://www.coursera.org/specializations/deep-learning", "type": "freemium", "platform": "Coursera"},
        {"title": "MIT 6.S191 – Introduction to Deep Learning", "url": "http://introtodeeplearning.com/", "type": "free", "platform": "MIT"},
    ],
    "Reinforcement Learning": [
        {"title": "Spinning Up in Deep RL – OpenAI", "url": "https://spinningup.openai.com/en/latest/", "type": "free", "platform": "OpenAI"},
        {"title": "Reinforcement Learning Specialization – Alberta (Coursera)", "url": "https://www.coursera.org/specializations/reinforcement-learning", "type": "freemium", "platform": "Coursera"},
    ],
    "Transfer Learning": [
        {"title": "Transfer Learning Guide – DeepLearning.AI", "url": "https://www.deeplearning.ai/short-courses/", "type": "free", "platform": "DeepLearning.AI"},
        {"title": "Transfer Learning with TensorFlow – Official Tutorial", "url": "https://www.tensorflow.org/tutorials/images/transfer_learning", "type": "free", "platform": "TensorFlow"},
    ],
    "Object Detection": [
        {"title": "Object Detection with YOLO – Ultralytics Docs", "url": "https://docs.ultralytics.com/", "type": "free", "platform": "Ultralytics"},
        {"title": "Object Detection Tutorial – PyTorch", "url": "https://pytorch.org/tutorials/intermediate/torchvision_tutorial.html", "type": "free", "platform": "PyTorch"},
    ],
    "Text Classification": [
        {"title": "Text Classification – Hugging Face Tutorial", "url": "https://huggingface.co/docs/transformers/tasks/sequence_classification", "type": "free", "platform": "Hugging Face"},
    ],
    "Sentiment Analysis": [
        {"title": "Sentiment Analysis with Hugging Face", "url": "https://huggingface.co/blog/sentiment-analysis-python", "type": "free", "platform": "Hugging Face"},
    ],
    "Recommendation System": [
        {"title": "Recommender Systems Specialization – Coursera", "url": "https://www.coursera.org/specializations/recommender-systems", "type": "freemium", "platform": "Coursera"},
        {"title": "Building Recommendation Systems – Google ML", "url": "https://developers.google.com/machine-learning/recommendation", "type": "free", "platform": "Google Developers"},
    ],
    "Feature Engineering": [
        {"title": "Feature Engineering for ML – Kaggle (Free Course)", "url": "https://www.kaggle.com/learn/feature-engineering", "type": "free", "platform": "Kaggle"},
    ],
    "Model Deployment": [
        {"title": "Deploying ML Models – Full Stack Deep Learning", "url": "https://fullstackdeeplearning.com/", "type": "free", "platform": "FSDL"},
        {"title": "ML Model Deployment – Udemy", "url": "https://www.udemy.com/course/deployment-of-machine-learning-models/", "type": "paid", "platform": "Udemy"},
    ],
    "A/B Testing": [
        {"title": "A/B Testing – Udacity Free Course", "url": "https://www.udacity.com/course/ab-testing--ud257", "type": "free", "platform": "Udacity"},
    ],
    "Data Warehousing": [
        {"title": "Data Warehousing & BI – Coursera", "url": "https://www.coursera.org/learn/dwdesign", "type": "freemium", "platform": "Coursera"},
        {"title": "Fundamentals of Data Engineering – Book", "url": "https://www.oreilly.com/library/view/fundamentals-of-data/9781098108298/", "type": "paid", "platform": "O'Reilly"},
    ],
    "Agile": [
        {"title": "Agile Fundamentals – Scrum Alliance", "url": "https://resources.scrumalliance.org/Article/agile-basics", "type": "free", "platform": "Scrum Alliance"},
        {"title": "Agile Project Management – Google on Coursera", "url": "https://www.coursera.org/learn/agile-project-management", "type": "freemium", "platform": "Coursera"},
    ],
    "Scrum": [
        {"title": "Scrum Guide – Official (Free)", "url": "https://scrumguides.org/scrum-guide.html", "type": "free", "platform": "scrumguides.org"},
        {"title": "Scrum Master Certification Prep – Udemy", "url": "https://www.udemy.com/course/scrum-master/", "type": "paid", "platform": "Udemy"},
    ],
    "System Design": [
        {"title": "System Design Primer – GitHub", "url": "https://github.com/donnemartin/system-design-primer", "type": "free", "platform": "GitHub"},
        {"title": "Grokking System Design – educative.io", "url": "https://www.educative.io/courses/grokking-the-system-design-interview", "type": "paid", "platform": "educative.io"},
        {"title": "System Design – ByteByteGo (YouTube)", "url": "https://www.youtube.com/@ByteByteGo", "type": "free", "platform": "YouTube"},
    ],
    "Event-Driven Architecture": [
        {"title": "Event-Driven Architecture – AWS Docs", "url": "https://aws.amazon.com/event-driven-architecture/", "type": "free", "platform": "AWS"},
        {"title": "Event-Driven Systems – Martin Fowler", "url": "https://martinfowler.com/articles/201701-event-driven.html", "type": "free", "platform": "martinfowler.com"},
    ],
}


# ─────────────────────────────────────────
# UTILITY FUNCTIONS
# ─────────────────────────────────────────

def get_resources(skill: str) -> list[dict]:
    """Return resources for a skill (case-insensitive lookup)."""
    for key in SKILL_RESOURCES:
        if key.lower() == skill.lower():
            return SKILL_RESOURCES[key]
    return []


def get_free_resources(skill: str) -> list[dict]:
    """Return only free resources for a given skill."""
    return [r for r in get_resources(skill) if r["type"] == "free"]


def skills_summary() -> None:
    """Print a quick summary of coverage."""
    total_skills = len(SKILL_RESOURCES)
    total_resources = sum(len(v) for v in SKILL_RESOURCES.values())
    print(f"Total skills mapped : {total_skills}")
    print(f"Total resource links: {total_resources}")
    platforms = {}
    for resources in SKILL_RESOURCES.values():
        for r in resources:
            platforms[r["platform"]] = platforms.get(r["platform"], 0) + 1
    print("\nTop platforms:")
    for p, count in sorted(platforms.items(), key=lambda x: -x[1])[:10]:
        print(f"  {p:<30} {count} resources")


if __name__ == "__main__":
    skills_summary()
    print("\n--- Example lookup: Python ---")
    for r in get_resources("JSON"):
        print(f"  [{r['type'].upper()}] {r['title']}")
        print(f"         {r['url']}")