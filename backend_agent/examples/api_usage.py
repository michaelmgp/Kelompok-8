#!/usr/bin/env python3
"""
Example script demonstrating the new standardized API endpoints
"""

import asyncio
import aiohttp
import json
from typing import Dict, Any

# API base URL
BASE_URL = "http://localhost:8000"

async def search_jobs_example():
    """Example of searching jobs using the new standardized API"""
    
    # Example search request matching the specification
    search_request = {
        "skills": ["java", "backend"],
        "keywords": ["spring boot", "api"],
        "budget_min": 800,
        "rate_type": "fixed",
        "remote": True,
        "duration_days_max": 30,
        "currency": "USD",
        "sources": ["upwork", "fiverr"],
        "sort_by": "relevance",
        "page_size": 10
    }
    
    print("🔍 Searching for jobs...")
    print(f"Request: {json.dumps(search_request, indent=2)}")
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(
                f"{BASE_URL}/api/v1/jobs/search",
                json=search_request
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    print("\n✅ Search successful!")
                    print(f"Found {len(result['jobs'])} jobs")
                    print(f"Request ID: {result['meta']['request_id']}")
                    print(f"Search took: {result['meta']['took_ms']}ms")
                    print(f"Sources hit: {result['meta']['sources_hit']}")
                    
                    # Display first job
                    if result['jobs']:
                        first_job = result['jobs'][0]
                        print(f"\n📋 First job:")
                        print(f"  Title: {first_job['title']}")
                        print(f"  Source: {first_job['source']}")
                        print(f"  Budget: {first_job.get('budget_min')} - {first_job.get('budget_max')} {first_job.get('currency', 'USD')}")
                        print(f"  Skills: {', '.join(first_job['skills'])}")
                        print(f"  Score: {first_job.get('score', 'N/A')}")
                        print(f"  URL: {first_job['url']}")
                        
                else:
                    print(f"❌ Search failed with status {response.status}")
                    error_text = await response.text()
                    print(f"Error: {error_text}")
                    
        except Exception as e:
            print(f"❌ Error during search: {e}")

async def get_job_details_example():
    """Example of getting job details"""
    
    # Example job ID (you would get this from a search)
    job_id = "upwork:1234567890"
    
    print(f"\n🔍 Getting details for job: {job_id}")
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(f"{BASE_URL}/api/v1/jobs/{job_id}") as response:
                if response.status == 200:
                    job = await response.json()
                    print("✅ Job details retrieved successfully!")
                    print(f"Title: {job['title']}")
                    print(f"Source: {job['source']}")
                    print(f"Description: {job.get('description', 'No description')[:100]}...")
                    print(f"Skills: {', '.join(job['skills'])}")
                    print(f"Budget: {job.get('budget_min')} - {job.get('budget_max')} {job.get('currency', 'USD')}")
                    print(f"Remote: {job.get('remote', 'Unknown')}")
                    print(f"Score: {job.get('score', 'N/A')}")
                    
                elif response.status == 404:
                    print("❌ Job not found")
                else:
                    print(f"❌ Failed to get job details: {response.status}")
                    error_text = await response.text()
                    print(f"Error: {error_text}")
                    
        except Exception as e:
            print(f"❌ Error getting job details: {e}")

async def get_trending_jobs_example():
    """Example of getting trending jobs"""
    
    print("\n🔥 Getting trending jobs...")
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(f"{BASE_URL}/api/v1/jobs/trending") as response:
                if response.status == 200:
                    jobs = await response.json()
                    print(f"✅ Found {len(jobs)} trending jobs")
                    
                    for i, job in enumerate(jobs[:3], 1):  # Show first 3
                        print(f"\n{i}. {job['title']}")
                        print(f"   Source: {job['source']}")
                        print(f"   Skills: {', '.join(job['skills'])}")
                        print(f"   Score: {job.get('score', 'N/A')}")
                        
                else:
                    print(f"❌ Failed to get trending jobs: {response.status}")
                    error_text = await response.text()
                    print(f"Error: {error_text}")
                    
        except Exception as e:
            print(f"❌ Error getting trending jobs: {e}")

async def get_platform_status_example():
    """Example of getting platform status"""
    
    print("\n📊 Getting platform status...")
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(f"{BASE_URL}/api/v1/platforms/status") as response:
                if response.status == 200:
                    status = await response.json()
                    print("✅ Platform status retrieved successfully!")
                    print(f"Coordinator initialized: {status['initialized']}")
                    print(f"Upwork enabled: {status['upwork_enabled']}")
                    print(f"Fiverr enabled: {status['fiverr_enabled']}")
                    print(f"Blockchain enabled: {status['blockchain_enabled']}")
                    
                else:
                    print(f"❌ Failed to get platform status: {response.status}")
                    error_text = await response.text()
                    print(f"Error: {error_text}")
                    
        except Exception as e:
            print(f"❌ Error getting platform status: {e}")

async def health_check_example():
    """Example of health check"""
    
    print("\n🏥 Checking system health...")
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(f"{BASE_URL}/health") as response:
                if response.status == 200:
                    health = await response.json()
                    print("✅ Health check successful!")
                    print(f"Status: {health['status']}")
                    print(f"Version: {health['version']}")
                    print(f"Services: {health['services']}")
                    
                else:
                    print(f"❌ Health check failed: {response.status}")
                    error_text = await response.text()
                    print(f"Error: {error_text}")
                    
        except Exception as e:
            print(f"❌ Error during health check: {e}")

async def main():
    """Main function to run all examples"""
    print("🚀 Job Platform Backend Agent - API Examples")
    print("=" * 50)
    
    # Check if server is running
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{BASE_URL}/health", timeout=5) as response:
                if response.status != 200:
                    print("❌ Server is not responding properly")
                    return
    except Exception as e:
        print(f"❌ Cannot connect to server at {BASE_URL}")
        print("Make sure the server is running with: python main.py")
        return
    
    print("✅ Server is running!")
    
    # Run examples
    await health_check_example()
    await get_platform_status_example()
    await search_jobs_example()
    await get_job_details_example()
    await get_trending_jobs_example()
    
    print("\n🎉 All examples completed!")

if __name__ == "__main__":
    asyncio.run(main()) 