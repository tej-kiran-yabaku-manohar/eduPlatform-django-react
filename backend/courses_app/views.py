from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError, NotFound
from .models import Course
from .serializer import CourseSerializer
from django.shortcuts import get_object_or_404

class EnrolledCoursesList(APIView):
    serializer_class = CourseSerializer

    def get(self, request):
        courses = Course.objects.all()            
        output = [{"id": course.course_id, "name": course.name, "progress": course.progress}
                  for course in courses]
        return Response(output)

    def post(self, request):
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            saved_course = serializer.instance
            response_data = {
                "id": saved_course.course_id,
                "name": saved_course.name,
                "progress": saved_course.progress
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request):
        updateCourse_id = request.data.get('course_id')
        if not updateCourse_id:
            raise ValidationError({'error': 'course_id is required'})

        course = get_object_or_404(Course, course_id=updateCourse_id)
        serializer = CourseSerializer(course, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request):
        delete_id = request.data.get('course_id')
        if not delete_id:
            raise ValidationError({'error': 'course_id is required'})

        try:
            course = get_object_or_404(Course, course_id=delete_id)
            course.delete()
            return Response({'message': 'Course deleted successfully', 'course_id': delete_id}, status=status.HTTP_204_NO_CONTENT)
        except Course.DoesNotExist:
            return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)
    

    


class AllCoursesList(APIView):
    def get(self, request):
        allCourses = [
            {
                'id': 1,
                'name': 'Introduction to Programming',
                'description': 'Learn the basics of programming with this beginner-friendly course.',
                'image': 'https://s3.amazonaws.com/coursera_assets/meta_images/generated/XDP/XDP~COURSE!~ball-state-university-introduction-to-programming-open-content/XDP~COURSE!~ball-state-university-introduction-to-programming-open-content.jpeg',
                'type': 'Programming',
                'difficulty': 'Beginner',
                'duration': '4 Weeks',
                'instructor': 'Jane Doe',
                'syllabus': ['Week 1: Basics', 'Week 2: Control Structures', 'Week 3: Functions', 'Week 4: Projects'],
                'reviews': [
                    {'reviewer': 'John Smith', 'comment': 'Very informative and well structured.', 'rating': 4},
                    {'reviewer': 'Emily White', 'comment': 'Great course for beginners!', 'rating': 5}
                ],
                'averageRating': 4.5
            },
            {
                'id': 2,
                'name': 'Data Science Fundamentals',
                'description': 'Dive into data science and learn essential concepts and techniques.',
                'image': 'https://s3.amazonaws.com/coursera_assets/meta_images/generated/XDP/XDP~SPECIALIZATION!~data-science-fundamentals/XDP~SPECIALIZATION!~data-science-fundamentals.jpeg',
                'type': 'Data Science',
                'difficulty': 'Intermediate',
                'duration': '8 Weeks',
                'instructor': 'John Doe',
                'syllabus': ['Week 1: Introduction', 'Week 2: Data Wrangling', 'Week 3: Machine Learning', 'Week 4: Project'],
                'reviews': [
                    {'reviewer': 'Alice Brown', 'comment': 'Challenging but rewarding!', 'rating': 3},
                    {'reviewer': 'Bob White', 'comment': 'Helped me get started with Data Science.', 'rating': 4}
                ],
                'averageRating': 3.5
            },
            {
                'id': 3,
                'name': 'Full Stack Web Development with React',
                'description': 'Dive deep into full stack web development using React, Node.js, and modern back-end technologies. Develop comprehensive skills by building real-world applications from the ground up.',
                'image': 'https://miro.medium.com/v2/resize:fit:1400/1*77ZqB9LosKxX0ngZy946Rw.jpeg',
                'type': 'Web Development',
                'difficulty': 'Advanced',
                'duration': '16 Weeks',
                'instructor': 'Alex Johnson',
                'syllabus': [
                    'Week 1: Introduction to Full Stack Development',
                    'Week 2: HTML, CSS, and JavaScript Essentials',
                    'Week 3: React Basics - Components and State',
                    'Week 4: Advanced React - Hooks and Context API',
                    'Week 5: State Management with Redux',
                    'Week 6: Routing in React with React Router',
                    'Week 7: Node.js and Express Basics',
                    'Week 8: Building APIs with Node.js',
                    'Week 9: Integrating MongoDB with Node.js',
                    'Week 10: User Authentication and Authorization',
                    'Week 11: React and Server-Side Rendering with Next.js',
                    'Week 12: Testing Your Applications with Jest and React Testing Library',
                    'Week 13: Advanced Backend Techniques - Caching, Security, and WebSockets',
                    'Week 14: Deploying Your Full Stack Application',
                    'Week 15: Project Work - Developing a Complete Application',
                    'Week 16: Capstone Project Presentation and Review'
                ],
                'reviews': [
                    {'reviewer': 'Emily Rose', 'comment': 'This course was a game-changer for my career as a developer. Highly detailed and well-structured.'},
                    {'reviewer': 'Jordan Smith', 'comment': 'Comprehensive and engaging. Alex does a fantastic job explaining complex topics in an understandable way.'}
                ],
                'averageRating': 4.5
            },
            {
                'id': 4,
                'name': 'Cybersecurity Fundamentals',
                'description': 'Explore the critical concepts of cybersecurity, including threat landscapes, risk management, and mitigation strategies.',
                'image': 'https://s3.amazonaws.com/coursera_assets/meta_images/generated/XDP/XDP~COURSE!~cyber-security-fundamentals/XDP~COURSE!~cyber-security-fundamentals.jpeg',
                'type': 'Cybersecurity',
                'difficulty': 'Beginner',
                'duration': '6 Weeks',
                'instructor': 'Alex Johnson',
                'syllabus': [
                    'Week 1: Introduction to Cybersecurity',
                    'Week 2: Types of Cyber Threats',
                    'Week 3: Cybersecurity Best Practices',
                    'Week 4: Implementing Network Security',
                    'Week 5: Cyber Incident Response',
                    'Week 6: Legal and Ethical Aspects in Cybersecurity'
                ],
                'reviews': [
                    {'reviewer': 'Linda Grey', 'comment': 'A thorough and engaging introduction to cybersecurity.'},
                    {'reviewer': 'Mark Black', 'comment': 'This course breaks down complex topics into understandable segments. Highly recommend for beginners!'}
                ],
                'averageRating': 5
            },
            {
                'id': 5,
                'name': 'Introduction to Databases',
                'description': 'Learn the fundamentals of databases, including database models, SQL, and data normalization.',
                'image': 'https://s3.amazonaws.com/coursera_assets/meta_images/generated/XDP/XDP~COURSE!~introduction-to-databases/XDP~COURSE!~introduction-to-databases.jpeg',
                'type': 'Database Management',
                'difficulty': 'Beginner',
                'duration': '6 Weeks',
                'instructor': 'Michael Lee',
                'syllabus': [
                    'Week 1: Database Concepts and Models',
                    'Week 2: SQL Basics',
                    'Week 3: Data Normalization',
                    'Week 4: Relational Databases',
                    'Week 5: Advanced SQL Queries',
                    'Week 6: Database Design and Implementation'
                ],
                'reviews': [
                    {'reviewer': 'Sophia Martinez', 'comment': 'The course was well-structured and provided a solid understanding of database management.', 'rating': 4},
                    {'reviewer': 'Daniel Roberts', 'comment': 'A comprehensive introduction to DBMS concepts and SQL. Ideal for beginners.', 'rating': 4.5}
                ],
                'averageRating': 4.25
            },
            {
                'id': 6,
                'name': 'JavaScript for Beginners',
                'description': 'Get started with JavaScript, learning basic syntax, control structures, and essential programming concepts.',
                'image': 'https://media.licdn.com/dms/image/D5612AQFzPrJRDUkC8Q/article-inline_image-shrink_1500_2232/0/1718609559709?e=1726704000&v=beta&t=FBfrLxdEJeijC4GaKxEwJeqBo-8ivn8DPdXy5Q6MEAA',
                'type': 'JavaScript',
                'difficulty': 'Beginner',
                'duration': '5 Weeks',
                'instructor': 'Sarah Lee',
                'syllabus': [
                    'Week 1: Introduction to JavaScript',
                    'Week 2: Basic Syntax and Variables',
                    'Week 3: Control Structures and Functions',
                    'Week 4: DOM Manipulation',
                    'Week 5: Event Handling and Project Work'
                ],
                'reviews': [
                    {'reviewer': 'James Green', 'comment': 'A fantastic starting point for learning JavaScript. Easy to follow and very informative.', 'rating': 4.5},
                    {'reviewer': 'Emily Clark', 'comment': 'Great for beginners. The exercises were practical and helped reinforce learning.', 'rating': 4}
                ],
                'averageRating': 4.25
            }, 
            {
                'id': 7,
                'name': 'Introduction to Cloud Computing',
                'description': 'Understand the principles of cloud computing, including various service models and deployment strategies.',
                'image': 'https://s3.amazonaws.com/coursera_assets/meta_images/generated/XDP/XDP~COURSE!~introduction-to-cloud/XDP~COURSE!~introduction-to-cloud.jpeg',
                'type': 'Cloud Computing',
                'difficulty': 'Beginner',
                'duration': '5 Weeks',
                'instructor': 'James Carter',
                'syllabus': [
                    'Week 1: Basics of Cloud Computing',
                    'Week 2: Cloud Service Models',
                    'Week 3: Cloud Deployment Models',
                    'Week 4: Cloud Security',
                    'Week 5: Case Studies and Practical Applications'
                ],
                'reviews': [
                    {'reviewer': 'Sophie Clarke', 'comment': 'An insightful course on cloud computing basics. Well-organized and easy to understand.', 'rating': 4},
                    {'reviewer': 'David Williams', 'comment': 'Good overview of cloud concepts with real-world examples. Recommended for beginners.', 'rating': 4.5}
                ],
                'averageRating': 5
            },
            {
                'id': 8,
                'name': 'Advanced Machine Learning Algorithms',
                'description': 'Dive into advanced machine learning algorithms, including deep learning, neural networks, and reinforcement learning.',
                'image': 'https://s3.amazonaws.com/coursera_assets/meta_images/generated/XDP/XDP~COURSE!~advanced-machine-learning-algorithms/XDP~COURSE!~advanced-machine-learning-algorithms.jpeg',
                'type': 'Machine Learning',
                'difficulty': 'Advanced',
                'duration': '8 Weeks',
                'instructor': 'Laura King',
                'syllabus': [
                    'Week 1: Introduction to Advanced ML Algorithms',
                    'Week 2: Neural Networks Basics',
                    'Week 3: Deep Learning Techniques',
                    'Week 4: Reinforcement Learning',
                    'Week 5: Hyperparameter Tuning',
                    'Week 6: Model Evaluation',
                    'Week 7: Practical Applications',
                    'Week 8: Capstone Project'
                ],
                'reviews': [
                    {'reviewer': 'Michael Green', 'comment': 'An in-depth course that covers cutting-edge machine learning techniques. Challenging but rewarding.', 'rating': 4.5},
                    {'reviewer': 'Emma Brown', 'comment': 'Advanced content presented in an accessible way. Great for deepening ML knowledge.', 'rating': 4.75}
                ],
                'averageRating': 4.63
            }
              ]

        return Response(allCourses)
