import os, httpx
import json
from typing import Dict, List, Any, Optional
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.tools import tool
from langchain.schema import BaseMessage, HumanMessage, AIMessage
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferWindowMemory
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser
import datetime
import time

load_dotenv()


MOCK_CLIENTS = [
    {
        "id": "C001",
        "name": "Priya Sharma",
        "email": "priya@example.com",
        "phone": "+91-9876543210",
        "enrolled_services": ["Yoga Classes"],
        "status": "Active"
    },
    {
        "id": "C002", 
        "name": "Amit Kumar",
        "email": "amit@example.com",
        "phone": "+91-9876543211",
        "enrolled_services": ["Fitness Training"],
        "status": "Active"
    },
    {
        "id": "C003",
        "name": "John Doe",
        "email": "john@example.com", 
        "phone": "+91-9876543212",
        "enrolled_services": ["Wellness Consultation"],
        "status": "Active"
    }
]

MOCK_ORDERS = [
    {
        "id": "ORD001",
        "client_id": "C001",
        "service": "Yoga Classes",
        "amount": 2000,
        "status": "Paid",
        "date": "2025-07-01",
        "payment_status": "Completed"
    },
    {
        "id": "ORD002",
        "client_id": "C002",
        "service": "Fitness Training", 
        "amount": 3000,
        "status": "Pending",
        "date": "2025-07-02",
        "payment_status": "Pending"
    },
    {
        "id": "ORD003",
        "client_id": "C003",
        "service": "Wellness Consultation",
        "amount": 1500,
        "status": "Paid",
        "date": "2025-07-03",
        "payment_status": "Completed"
    }
]

MOCK_COURSES = [
    {
        "id": "YOGA001",
        "name": "Yoga Classes",
        "instructor": "Priya Instructor",
        "schedule": "Monday, Wednesday, Friday - 9:00 AM to 10:00 AM",
        "availability": "Available",
        "price": 2000,
        "duration": "1 month"
    },
    {
        "id": "FITNESS001", 
        "name": "Fitness Training",
        "instructor": "Amit Trainer",
        "schedule": "Tuesday, Thursday, Saturday - 6:00 PM to 7:00 PM",
        "availability": "Available",
        "price": 3000,
        "duration": "1 month"
    },
    {
        "id": "WELLNESS001",
        "name": "Wellness Consultation",
        "instructor": "Dr. Wellness",
        "schedule": "By appointment - Monday to Friday",
        "availability": "Available",
        "price": 1500,
        "duration": "1 session"
    }
]

API_BASE = os.getenv("AGENT1_API_BASE", "http://127.0.0.1:8000/api")

@tool
def search_client(query: str) -> str:
    """Search for a client by name, email, or phone."""
    try:
        r = httpx.get(f"{API_BASE}/agent1/clients/search/", params={'q': query}, timeout=10)
        r.raise_for_status()
        data = r.json()
        return json.dumps(data, indent=2) if data else "No client found."
    except Exception as e:
        return f"Error contacting backend: {e}"

@tool
def check_order_status(order_id: str) -> str:
    """Check the status and payment information for a specific order ID."""
    order_id = order_id.upper().strip()
    for order in MOCK_ORDERS:
        if order["id"] == order_id:
            client = next((c for c in MOCK_CLIENTS if c["id"] == order["client_id"]), None)
            client_name = client["name"] if client else "Unknown"
            return f"""Order Details:
- Order ID: {order['id']}
- Client: {client_name}
- Service: {order['service']}
- Amount: ₹{order['amount']}
- Order Status: {order['status']}
- Payment Status: {order['payment_status']}
- Date: {order['date']}"""
    return f"Order {order_id} not found. Please check the order ID and try again."

@tool
def get_course_schedule(service_name: str = "") -> str:
    """Get the schedule and availability for a specific service or all available services."""
    if service_name:
        service_name = service_name.lower().strip()
        for course in MOCK_COURSES:
            if service_name in course["name"].lower():
                return f"""Course Details:
- Service: {course['name']}
- Instructor: {course['instructor']}
- Schedule: {course['schedule']}
- Availability: {course['availability']}
- Price: ₹{course['price']}
- Duration: {course['duration']}"""
    
    # Return all courses if no specific service requested
    schedule_info = "📅 Available Services and Schedules:\n\n"
    for course in MOCK_COURSES:
        schedule_info += f"🔸 {course['name']}\n"
        schedule_info += f"   Instructor: {course['instructor']}\n"
        schedule_info += f"   Schedule: {course['schedule']}\n"
        schedule_info += f"   Price: ₹{course['price']} ({course['duration']})\n"
        schedule_info += f"   Status: {course['availability']}\n\n"
    
    return schedule_info

@tool
def get_service_info(service_type: str = "") -> str:
    """Get information about available services, pricing, and descriptions.
    Use this tool when customers ask about services, pricing, or general information."""
    
    if service_type:
        service_type = service_type.lower().strip()
        for course in MOCK_COURSES:
            if service_type in course["name"].lower():
                return f"""Service Information:
- Service: {course['name']}
- Price: ₹{course['price']}
- Duration: {course['duration']}
- Instructor: {course['instructor']}
- Availability: {course['availability']}
- Schedule: {course['schedule']}"""
    
    # Return all services if no specific type requested
    services_info = "🎯 Our Services:\n\n"
    for course in MOCK_COURSES:
        services_info += f"🔸 {course['name']}\n"
        services_info += f"   Price: ₹{course['price']} ({course['duration']})\n"
        services_info += f"   Instructor: {course['instructor']}\n"
        services_info += f"   Availability: {course['availability']}\n\n"
    
    return services_info

@tool
def create_enquiry(name: str, email: str, phone: str, service: str, message: str) -> str:
    """Create a new customer enquiry. 
    Use this tool when customers want to register interest or ask questions about services."""
    
    enquiry_id = f"ENQ{int(time.time())}"
    
    enquiry_data = {
        "id": enquiry_id,
        "name": name,
        "email": email,
        "phone": phone,
        "service": service,
        "message": message,
        "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": "New"
    }
    
    # In production, save to Django database
    # For now, just return confirmation
    return f"""Enquiry Created Successfully!
- Enquiry ID: {enquiry_id}
- Name: {name}
- Email: {email}
- Phone: {phone}
- Service Interest: {service}
- Message: {message}
- Status: New

Our team will contact you within 24 hours. Thank you for your interest!"""

# =============================================================================
# AGENT CONFIGURATION
# =============================================================================

class Agent1CustomerSupport:
    def __init__(self):
        self.llm = ChatOllama(model="llama3-groq-tool-use:8b", base_url="http://127.0.0.1:11434",
            temperature=0.2,
            num_predict=512,  # Limit response length
            timeout=30  # 30 second timeout
        )
        
        self.tools = [
            search_client,
            check_order_status,
            get_course_schedule,
            get_service_info,
            create_enquiry
        ]
        
        self.memory = ConversationBufferWindowMemory(
            memory_key="chat_history",
            return_messages=True,
            k=10  # Keep last 10 interactions
        )
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are Agent1, a helpful customer support agent for a service business. 
            
Your role is to assist customers with:
- Finding client information and account details
- Checking order status and payment information  
- Providing course schedules and availability
- Sharing service information and pricing
- Creating new customer enquiries

IMPORTANT INSTRUCTIONS:
1. Always be polite, professional, and helpful
2. Use the available tools to provide accurate information
3. If you can't find specific information, suggest alternatives
4. Keep responses concise but informative
5. Never make up information - only use data from tools
6. If asked about payments, always check order status first
7. For scheduling questions, use the course schedule tool
8. For new customers, offer to create an enquiry

Business Context:
- You work for a service business offering yoga classes, fitness training, and wellness consultations
- Customers may ask about their orders, payments, schedules, or want to sign up for services
- Always try to be helpful and guide customers to the right solution

Example responses:
- For client searches: "Let me look up your information..."
- For order status: "I'll check your order status right away..."
- For schedules: "Here are our current class schedules..."
- For services: "We offer several services, let me share the details..."
"""),
            MessagesPlaceholder(variable_name="chat_history", optional=True),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ])
        
        # Create the agent
        self.agent = create_tool_calling_agent(self.llm, self.tools, self.prompt)
        
        # Create executor with safety limits
        self.executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            memory=self.memory,
            verbose=True,
            handle_parsing_errors=True,
            max_iterations=5,  # Prevent infinite loops
            max_execution_time=60,  # 1 minute timeout
            early_stopping_method="generate"
        )
    
    def chat(self, message: str) -> str:
        """Process a customer message and return response."""
        try:
            response = self.executor.invoke({"input": message})
            return response.get("output", "I apologize, but I couldn't process your request. Please try again.")
        except Exception as e:
            return f"I apologize for the technical issue. Please try rephrasing your question. Error: {str(e)}"
    
    def reset_memory(self):
        """Reset conversation memory."""
        self.memory.clear()

# =============================================================================
# INTERACTIVE TESTING
# =============================================================================

def test_agent1():
    """Test Agent1 with sample queries."""
    print("🚀 Starting Agent1 - LangChain Direct Implementation")
    print("=" * 60)
    
    # Initialize agent
    agent = Agent1CustomerSupport()
    
    # Test queries
    test_queries = [
        "Hello! What services do you offer?",
        "Can you find information about Priya Sharma?",
        "What's the status of order ORD002?",
        "What are the yoga class schedules?",
        "How much does fitness training cost?",
        "I want to enquire about wellness consultation"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n📝 Test {i}: {query}")
        print("-" * 40)
        
        try:
            response = agent.chat(query)
            print(f"🤖 Agent1: {response}")
            print("✅ Success!")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("\n" + "=" * 60)
    
    print("\n🎯 Agent1 Testing Complete!")
    print("Agent1 is ready for Django integration!")

def interactive_mode():
    """Interactive mode for testing Agent1."""
    print("🚀 Agent1 Interactive Mode")
    print("=" * 60)
    print("Type 'quit' to exit, 'reset' to clear memory")
    print("Ask me about clients, orders, schedules, or services!\n")
    
    agent = Agent1CustomerSupport()
    
    while True:
        try:
            user_input = input("💤 You: ").strip()
            
            if user_input.lower() == 'quit':
                print("👋 Thanks for using Agent1!")
                break
            elif user_input.lower() == 'reset':
                agent.reset_memory()
                print("🔄 Memory reset. Starting fresh conversation.")
                continue
            elif not user_input:
                continue
            
            print(f"🤖 Agent1: {agent.chat(user_input)}")
            print()
            
        except KeyboardInterrupt:
            print("\n👋 Thanks for using Agent1!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("Agent1 - Customer Support System")
    print("Choose mode:")
    print("1. Run automated tests")
    print("2. Interactive mode") 
    print("3. Both")
    
    choice = input("\nEnter choice (1/2/3): ").strip()
    
    if choice == "1":
        test_agent1()
    elif choice == "2":
        interactive_mode()
    elif choice == "3":
        test_agent1()
        print("\n" + "=" * 60)
        print("Now starting interactive mode...")
        interactive_mode()
    else:
        print("Invalid choice. Running automated tests...")
        test_agent1()
