# Go-CRM Frontend Structure

A comprehensive Next.js 14 frontend for the Go-CRM application with full TypeScript support and modern React patterns.

## 🏗️ **Architecture**

### **Tech Stack**
- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS v4
- **State Management**: React Context API + Custom Hooks
- **API Communication**: Custom fetch wrapper with error handling
- **Authentication**: JWT-based (ready for implementation)

## 📁 **Directory Structure**

```
frontend/src/
├── app/                          # Next.js App Router pages
│   ├── (auth)/                   # Authentication routes (future)
│   ├── dashboard/                # Main dashboard page
│   ├── contacts/                 # Contact management pages
│   ├── apex/                     # Apex Research pages
│   ├── super-researcher/         # Super Researcher pages
│   ├── research/                 # Research pipeline pages
│   ├── todos/                    # Todo management pages
│   ├── communications/           # Communication history pages
│   ├── layout.tsx                # Root layout with providers
│   ├── page.tsx                  # Home page (redirects to dashboard)
│   └── globals.css               # Global styles
├── components/                   # React components
│   ├── ui/                       # Reusable UI components
│   ├── layout/                   # Layout components (Sidebar, Header)
│   ├── contacts/                 # Contact-specific components
│   ├── research/                 # Research-related components
│   ├── todos/                    # Todo components
│   └── communications/           # Communication components
├── lib/                          # Core library code
│   ├── api/                      # API client and endpoints
│   ├── hooks/                    # Custom React hooks
│   ├── types/                    # TypeScript type definitions
│   ├── utils/                    # Utility functions
│   └── context/                  # React context providers
└── styles/                       # Additional styles
```

## 🔌 **API Integration**

### **API Client Structure**
- **Base Client**: Handles authentication, errors, and request/response processing
- **Endpoint Modules**: Organized by feature (contacts, apex, super-researcher, todos)
- **Type Safety**: Full TypeScript support with proper error handling

### **API Endpoints**
```typescript
// Contacts
GET    /api/contacts/index              - Get all contacts with filters
GET    /api/contacts/moreinfo/:id       - Get contact details
POST   /api/contacts/add                - Create new contact
POST   /api/contacts/update/:id         - Update contact
DELETE /api/contacts/delete/:id         - Delete contact
POST   /api/contacts/send-email/:id     - Send email to contact
POST   /api/contacts/send-sms/:id       - Send SMS to contact
GET    /api/contacts/communication-logs - Get all communication logs

// Apex Research
GET    /api/apex/contacts               - Get all apex contacts
POST   /api/apex/contacts               - Create apex contact
POST   /api/apex/contacts/:id/promote   - Promote to staged lead

// Super Researcher
GET    /api/super-researcher/           - Get all researchers
POST   /api/super-researcher/           - Create researcher
PUT    /api/super-researcher/:id        - Update researcher
DELETE /api/super-researcher/:id        - Delete researcher

// Todos
GET    /api/todos/                      - Get all todos
POST   /api/todos/                      - Create todo
PUT    /api/todos/:id                   - Update todo
DELETE /api/todos/:id                   - Delete todo
```

## 🎨 **Component Library**

### **UI Components** (`components/ui/`)
- **Button**: Variants (primary, secondary, danger, success, ghost) + sizes
- **Input**: Form input with labels and error handling
- **Select**: Dropdown select with options
- **Textarea**: Multi-line text input
- **Modal**: Accessible modal dialog
- **Card**: Content container with optional header/actions
- **Badge**: Status indicators with color variants
- **Loader**: Loading spinner with size options

### **Layout Components** (`components/layout/`)
- **MainLayout**: Main app layout with sidebar and header
- **Sidebar**: Navigation sidebar with route highlighting
- **Header**: Top header with user info and logout

### **Feature Components** (`components/`)
- **ContactList**: Contact list with filtering and search
- **ContactForm**: Contact creation/editing form
- **TodoList**: Todo list with filtering and actions
- **ResearchPipeline**: Kanban-style pipeline view for research leads

## 🪝 **Custom Hooks**

### **Data Hooks** (`lib/hooks/`)
- **useContacts**: Contact data and operations
- **useContact**: Single contact data
- **useContactOperations**: Contact CRUD operations
- **useApexResearch**: Apex research contacts
- **useSuperResearcher**: Super researcher data
- **useResearchPipeline**: Research pipeline management
- **useTodos**: Todo management
- **useCommunications**: Communication logs
- **useAuth**: Authentication state and methods

## 🎯 **Type Definitions**

### **Core Types** (`lib/types/`)
```typescript
// Contact Types
Contact, ContactFormData, ContactFilters, SentEmail, SentSms

// Research Types
ApexContact, ApexFormData, SuperResearcher, SuperResearcherFormData

// Todo Types
Todo, TodoFormData, TodoFilters

// API Types
ApiResponse, ApiError, PaginatedResponse
```

## 🛠️ **Utilities**

### **Helper Functions** (`lib/utils/`)
- **constants.ts**: App constants, route definitions, color mappings
- **formatting.ts**: Date/time formatting, phone number formatting
- **validation.ts**: Email, phone, URL validation
- **helpers.ts**: Debounce, throttle, ID generation, etc.

## 🚀 **Getting Started**

### **Prerequisites**
- Node.js 18+ installed
- Backend API running on port 8000

### **Installation**
```bash
# Install dependencies
npm install

# Copy environment file
cp .env.example .env.local

# Update API URL in .env.local if needed
```

### **Development**
```bash
# Run development server
npm run dev

# Build for production
npm run build

# Start production server
npm start
```

## 🔐 **Authentication**

### **Current Status**
- Basic auth context provided
- Mock login functionality
- Ready for JWT implementation

### **Implementation Guide**
1. Add login endpoint to backend API
2. Update `useAuth` hook to call real API
3. Implement protected route middleware
4. Add refresh token handling

## 📊 **Key Features**

### **Dashboard**
- Overview statistics
- Recent contacts preview
- Pending tasks list
- Research pipeline summary

### **Contact Management**
- Full CRUD operations
- Advanced filtering and search
- Lead classification tracking
- Email and SMS integration

### **Research Pipeline**
- Staged leads management
- Active leads tracking
- Conversion workflow
- Apex and Super Researcher integration

### **Communication Tracking**
- Email history
- SMS logs
- Combined timeline
- Contact-specific communications

### **Task Management**
- Create, update, delete todos
- Priority levels
- Completion tracking
- Filtering by status

## 🎨 **Styling**

### **Color Scheme**
- **Primary**: Blue (#3B82F6)
- **Success**: Green (#10B981)
- **Warning**: Yellow (#F59E0B)
- **Danger**: Red (#EF4444)
- **Info**: Purple (#8B5CF6)

### **Responsive Design**
- Mobile-first approach
- Breakpoints: sm (640px), md (768px), lg (1024px)
- Collapsible sidebar on mobile
- Touch-friendly buttons

## 🔄 **State Management**

### **Strategy**
- **Local State**: useState for component-specific state
- **Global State**: React Context for auth and toasts
- **Server State**: Custom hooks with API calls
- **URL State**: Query parameters for filters/search

### **Data Flow**
1. Component uses custom hook
2. Hook calls API endpoint
3. Data returned and cached
4. Component re-renders with new data
5. User actions trigger optimistic updates

## 🚦 **Error Handling**

### **API Errors**
- Automatic error message display
- User-friendly error messages
- Fallback UI for failed requests
- Retry mechanisms for failed calls

### **Form Validation**
- Client-side validation
- Real-time error feedback
- Disabled submit buttons during loading
- Clear error messages

## 📈 **Performance Optimization**

### **Optimization Techniques**
- Code splitting by route
- Lazy loading for heavy components
- Image optimization with Next.js Image
- Debounced search inputs
- Pagination for large lists

## 🧪 **Testing**

### **Recommended Setup**
```bash
# Install testing dependencies
npm install --save-dev jest @testing-library/react @testing-library/jest-dom

# Run tests
npm test
```

## 🚢 **Deployment**

### **Build Process**
```bash
# Create production build
npm run build

# Test production build locally
npm start
```

### **Environment Variables**
Ensure all required environment variables are set in production:
- `NEXT_PUBLIC_API_URL`: Backend API URL

## 📝 **Development Notes**

### **Code Style**
- Use TypeScript for all new files
- Follow existing component patterns
- Implement proper error handling
- Add loading states for async operations
- Use proper accessibility attributes

### **Best Practices**
- Keep components small and focused
- Use custom hooks for reusable logic
- Implement proper error boundaries
- Optimize images and assets
- Follow React best practices

## 🔧 **Troubleshooting**

### **Common Issues**
1. **API Connection Error**: Check that backend is running and CORS is configured
2. **Type Errors**: Run `npm run build` to catch TypeScript errors
3. **Styling Issues**: Clear Next.js cache: `rm -rf .next`
4. **Hot Reload Issues**: Restart dev server

## 📚 **Additional Resources**

- [Next.js Documentation](https://nextjs.org/docs)
- [React Documentation](https://react.dev)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [TypeScript Handbook](https://www.typescriptlang.org/docs)

---

**Note**: This frontend is designed to work with the Django REST backend. Ensure the backend API is running and properly configured before starting the frontend development server.