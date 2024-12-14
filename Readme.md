Frontend:

src/
├── components/                   # Reusable components
│   ├── chat/                     # Chat-specific components
│   │   ├── ChatBox.js
│   │   ├── ChatMessage.js
│   │   ├── ChatInput.js
│   └── common/                   # Shared components
│       ├── Sidebar.js            # Persistent sidebar
│       ├── Navbar.js             # Optional navbar
│       ├── PageHeader.js         # Header for Notion-like pages
├── features/                     # Feature-specific logic
│   ├── auth/                     # Authentication-related logic
│   ├── chat/                     # Chat service logic
│   └── courses/                  # Course-related logic
│       ├── CourseService.js
│       ├── courseSlice.js        # Redux state for courses
├── layouts/                      # Layout components
│   ├── MainLayout.js             # Layout with sidebar for all pages
├── pages/                        # Page-level components
│   ├── ChatPage.js               # Chat interface
│   ├── CoursesPage.js            # Notion-like page for courses
│   ├── PrepPlansPage.js          # Page for prep plans
│   ├── JobRolesPage.js           # Page for job roles
│   ├── NotFoundPage.js           # 404 page
├── store/                        # State management
├── services/                     # API integration
├── App.js                        # App entry point with routing
├── index.js                      # React DOM entry point


Backend:
backend/
├── auth/                         # Authentication service
│   ├── AuthController.js         # Handles login, signup, token generation
│   ├── AuthService.js            # Business logic for authentication
│   ├── AuthRoutes.js             # Routes for auth APIs
├── content/                      # Content management service
│   ├── ContentController.js      # Handles requests for courses, prep plans
│   ├── ContentService.js         # Logic for fetching/storing content
│   ├── ContentRoutes.js          # Routes for content APIs
├── chat/                         # Chat service
│   ├── ChatController.js         # Handles incoming chat messages
│   ├── ChatService.js            # Logic for chat history, user context
│   ├── ChatRoutes.js             # Routes for chat APIs
├── decision-engine/              # Decision Engine microservice
│   ├── DecisionEngineController.js  # Orchestrates LLM calls
│   ├── LLMService.js             # Communicates with the LLM API
│   ├── DecisionEngineRoutes.js   # Routes for Decision Engine APIs
├── db/                           # Database connections and models
│   ├── models/                   # Sequelize/Mongoose models
│   │   ├── User.js
│   │   ├── Course.js
│   │   ├── ChatHistory.js
│   ├── db.js                     # Database initialization
├── middleware/                   # Shared middleware
│   ├── errorMiddleware.js        # Global error handling
│   ├── authMiddleware.js         # Protect routes with JWT
│   ├── loggingMiddleware.js      # Logs incoming requests
├── routes/                       # Global route definitions
│   ├── index.js                  # Combines all service routes
├── utils/                        # Helper functions
│   ├── responseHelper.js         # Formats API responses
│   ├── validationHelper.js       # Input validation utilities
├── server.js                     # App entry point
├── package.json                  # Dependencies